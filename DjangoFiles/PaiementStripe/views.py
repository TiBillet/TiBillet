import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
import stripe
from django.utils import timezone
from django.views import View
from rest_framework import serializers

from BaseBillet.models import Configuration, LigneArticle, Paiement_stripe, Reservation
from django.utils.translation import gettext, gettext_lazy as _

import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class creation_paiement_stripe():

    def __init__(self,
                 user: User,
                 liste_ligne_article: list,
                 metadata: dict,
                 reservation: (Reservation, None),
                 source: str,
                 absolute_domain: str
                 ) -> None:

        self.user = user
        self.email_paiement = user.email
        self.absolute_domain = absolute_domain
        self.liste_ligne_article = liste_ligne_article
        self.metadata = metadata
        self.reservation = reservation
        self.source = source
        self.configuration = Configuration.get_solo()

        self.total = self._total()
        self.metadata_json = json.dumps(self.metadata)
        self.paiement_stripe_db = self._paiement_stripe_db()
        self.stripe_api_key = self._stripe_api_key()
        self.line_items = self._line_items()
        self.return_url = self._return_url()
        self.checkout_session = self._checkout_session()


    def _total(self):
        total = 0
        for ligne in self.liste_ligne_article:
            total += float(ligne.qty) * float(ligne.pricesold.prix)
        return total

    def _paiement_stripe_db(self):

        paiementStripeDb = Paiement_stripe.objects.create(
            user=self.user,
            total=self.total,
            metadata_stripe=self.metadata_json,
            reservation=self.reservation,
            source=self.source,
        )

        for ligne_article in self.liste_ligne_article:
            ligne_article: LigneArticle
            ligne_article.paiement_stripe = paiementStripeDb
            ligne_article.save()

        return paiementStripeDb

    def _stripe_api_key(self):
        api_key = self.configuration.get_stripe_api()
        if api_key:
            stripe.api_key = api_key
            return stripe.api_key
        else :
            raise serializers.ValidationError(_(f"No Stripe Api Key in configuration"))

    def _line_items(self):
        line_items = []
        for ligne in self.liste_ligne_article:
            ligne: LigneArticle
            line_items.append(
                {
                    "price": f"{ligne.pricesold.get_id_price_stripe()}",
                    "quantity": int(ligne.qty),
                }
            )
        return line_items
    def _return_url(self):
        '''
        Si la source est le QRCode, alors c'est encore le model MVC de django qui g??re ??a.
        Sinon, c'est un paiement via la billetterie vue.js
        :return:
        '''

        if self.source == Paiement_stripe.QRCODE :
            return "/api/webhook_stripe/"
        else :
            return "/stripe/return/"

    def _checkout_session(self):
        checkout_session = stripe.checkout.Session.create(
            success_url=f'{self.absolute_domain}{self.return_url}{self.paiement_stripe_db.uuid}',
            cancel_url=f'{self.absolute_domain}{self.return_url}{self.paiement_stripe_db.uuid}',
            payment_method_types=["card"],
            customer_email=f'{self.user.email}',
            line_items=self.line_items,
            mode='payment',
            metadata=self.metadata,
            client_reference_id=f"{self.user.pk}",
        )
        print("-"*40)
        print(f"Cr??ation d'un nouveau paiment stripe. Metadata : {self.metadata}")
        print(f"checkout_session.id {checkout_session.id} payment_intent : {checkout_session.payment_intent}")
        print("-"*40)
        self.paiement_stripe_db.payment_intent_id = checkout_session.payment_intent
        self.paiement_stripe_db.checkout_session_id_stripe = checkout_session.id
        self.paiement_stripe_db.status = Paiement_stripe.PENDING
        self.paiement_stripe_db.save()

        return checkout_session

    def is_valid(self):
        if self.checkout_session.id and \
                self.checkout_session.url:
            return True
        else:
            return False

    def redirect_to_stripe(self):
        return HttpResponseRedirect(self.checkout_session.url)

'''
# On v??rifie que les m??tatada soient les meme dans la DB et chez Stripe.
def metatadata_valid(paiement_stripe_db: Paiement_stripe, checkout_session):
    metadata_stripe_json = checkout_session.metadata
    metadata_stripe = json.loads(str(metadata_stripe_json))

    metadata_db_json = paiement_stripe_db.metadata_stripe
    metadata_db = json.loads(metadata_db_json)

    try:
        assert metadata_stripe == metadata_db
        assert set(metadata_db.keys()) == set(metadata_stripe.keys())
        for key in set(metadata_stripe.keys()):
            assert metadata_db[key] == metadata_stripe[key]
        return True
    except:
        logger.error(f"{timezone.now()} "
                     f"retour_stripe {paiement_stripe_db.uuid} : "
                     f"metadata ne correspondent pas : {metadata_stripe} {metadata_db}")
        return False


class retour_stripe(View):

    def get(self, request, uuid_stripe):
        paiement_stripe = get_object_or_404(Paiement_stripe, uuid=uuid_stripe)

        if paiement_stripe.traitement_en_cours:
            return HttpResponse(
                'traitement_en_cours')

        if paiement_stripe.reservation:
            if paiement_stripe.reservation.status == Reservation.PAID_ERROR:
                return HttpResponse(
                    "Erreur dans l'envoie du mail. Merci de v??rifier l'adresse")

            if paiement_stripe.status == Paiement_stripe.VALID or paiement_stripe.reservation.status == Reservation.VALID:
                return HttpResponse(
                    'Paiement d??ja valid?? !')

        configuration = Configuration.get_solo()
        stripe.api_key = configuration.get_stripe_api()

        print(paiement_stripe.status)
        if paiement_stripe.status != Paiement_stripe.VALID:

            checkout_session = stripe.checkout.Session.retrieve(paiement_stripe.checkout_session_id_stripe)

            # on v??rfie que les metatada soient coh??rentes. #NTUI !
            if metatadata_valid(paiement_stripe, checkout_session):

                if checkout_session.payment_status == "unpaid":
                    paiement_stripe.status = Paiement_stripe.PENDING
                    if datetime.now().timestamp() > checkout_session.expires_at:
                        paiement_stripe.status = Paiement_stripe.EXPIRE
                    paiement_stripe.save()
                    return HttpResponse(
                        f'stripe : {checkout_session.payment_status} - paiement : {paiement_stripe.status}')

                elif checkout_session.payment_status == "paid":

                    # le .save() lance le process pre_save BaseBillet.models.send_to_cashless
                    # qui modifie le status de chaque ligne
                    # et envoie les informations au serveur cashless.
                    # si valid?? par le serveur cashless, alors la ligne sera VALID.
                    # Si toute les lignes sont VALID, le paiement_stripe sera aussi VALID
                    # grace au post_save BaseBillet.models.check_status_stripe

                    logger.info(f"retour_stripe - checkout_session.payment_status : {checkout_session.payment_status}")
                    paiement_stripe.status = Paiement_stripe.PAID
                    paiement_stripe.last_action = timezone.now()
                    paiement_stripe.traitement_en_cours = True
                    paiement_stripe.save()
                    logger.info(f"retour_stripe - paiement_stripe.save() {paiement_stripe.status}")


                else:
                    paiement_stripe.status = Paiement_stripe.CANCELED
                    paiement_stripe.save()
            else:
                raise Http404

        # on v??rifie que le status n'ai pas chang??
        paiement_stripe.refresh_from_db()
        # import ipdb; ipdb.set_trace()

        # si c'est depuis le qrcode, on renvoie vers la vue mobile :
        if paiement_stripe.source == Paiement_stripe.QRCODE:

            # SI le paiement est valide, c'est que les presave et postsave
            # ont valid?? la r??ponse du serveur cashless pour les recharges

            if paiement_stripe.status == Paiement_stripe.VALID:
                # on boucle ici pour r??cuperer l'uuid de la carte.
                for ligne_article in paiement_stripe.lignearticle_set.all():
                    if ligne_article.carte:
                        messages.success(request, f"Paiement valid??. Merci !")
                        return HttpResponseRedirect(f"/qr/{ligne_article.carte.uuid}#success")

            else:
                # on boucle ici pour r??cuperer l'uuid de la carte.
                for ligne_article in paiement_stripe.lignearticle_set.all():
                    if ligne_article.carte:
                        messages.error(request,
                                       f"Un probl??me de validation de paiement a ??t?? detect??. "
                                       f"Merci de v??rifier votre moyen de paiement et/ou contactez un responsable.")
                        return HttpResponseRedirect(f"/qr/{ligne_article.carte.uuid}#erreurpaiement")

        elif paiement_stripe.source == Paiement_stripe.API_BILLETTERIE:
            if paiement_stripe.reservation:
                if paiement_stripe.reservation.status == Reservation.VALID:
                    return HttpResponse(
                        'Paiement d??ja valid?? !')
            if paiement_stripe.status == Paiement_stripe.VALID:
                return HttpResponse(
                    'Paiement d??ja valid?? !')

            elif paiement_stripe.status == Paiement_stripe.PAID:
                logger.info(f"Paiement_stripe.API_BILLETTERIE  : {paiement_stripe.status}")
                return HttpResponse(
                    'Paiement okay, on lance les process de validation.')

        raise Http404(f'{paiement_stripe.status}')



class webhook_stripe(View):
    def get(self, request):
        print(f"webhook_stripe GET")
        return  HttpResponse(f'ok')

    def post(self, request):
        endpoint_secret = 'whsec_1Urn98yUMsgwdXA7vhN5dwDTRQLD2vmD'
        event = None
        payload = request.data
        sig_header = request.headers['STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        # Handle the event
        print('Unhandled event type {}'.format(event['type']))

        print(f"webhook_stripe POST {event}")
        return  HttpResponse(f'ok {event}')
'''
