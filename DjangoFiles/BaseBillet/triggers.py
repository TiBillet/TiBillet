import requests
# from django.db import connection
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# from django.utils import timezone

# from ApiBillet.thread_mailer import ThreadMaileur
from django.utils import timezone

from BaseBillet.models import Reservation, LigneArticle, Ticket, Product, Configuration, Paiement_stripe, Membership
from BaseBillet.tasks import send_membership_to_cashless

# from TiBillet import settings

import logging
logger = logging.getLogger(__name__)


class action_article_paid_by_categorie:
    '''
    BILLET, PACK, RECHARGE_CASHLESS, VETEMENT, MERCH, ADHESION = 'B', 'P', 'R', 'T', 'M', 'A'
        CATEGORIE_ARTICLE_CHOICES = [
            (BILLET, _('Billet')),
            (PACK, _("Pack d'objets")),
            (RECHARGE_CASHLESS, _('Recharge cashless')),
            (VETEMENT, _('Vetement')),
            (MERCH, _('Merchandasing')),
            (ADHESION, ('Adhésion')),
        ]

    Trigged action by categorie when Article is PAID
    '''

    def __init__(self, ligne_article:LigneArticle, **kwargs):
        self.ligne_article = ligne_article
        self.categorie = self.ligne_article.pricesold.productsold.product.categorie_article

        self.data_for_cashless = {}
        if ligne_article.paiement_stripe :
            self.data_for_cashless = {'uuid_commande': ligne_article.paiement_stripe.uuid }

        try:
            # on met en majuscule et on rajoute _ au début du nom de la catégorie.
            trigger_name = f"_{self.categorie.upper()}"
            logger.info(f"category_trigger launched - ligne_article : {self.ligne_article} - trigger_name : {trigger_name}")
            trigger = getattr(self, f"trigger{trigger_name}")
            trigger()
        except AttributeError:
            logger.info(f"Pas de trigger pour la categorie {self.categorie}")
        except Exception as exc:
            logger.error(f"category_trigger ERROR : {exc} - {type(exc)}")

    # Category BILLET
    def trigger_B(self):
        logger.info(f"TRIGGER BILLET")

    # Category Free Reservation
    def trigger_F(self):
        logger.info(f"TRIGGER FREE RESERVATION")

    # Category RECHARGE_CASHLESS
    def trigger_R(self):
        logger.info(f"TRIGGER RECHARGE_CASHLESS")
        configuration = Configuration.get_solo()
        if not configuration.server_cashless or not configuration.key_cashless:
            raise Exception(f'Pas de configuration cashless')

        self.data_for_cashless['card_uuid'] = self.ligne_article.carte.uuid
        self.data_for_cashless['qty'] = self.ligne_article.pricesold.prix

        data = self.data_for_cashless

        sess = requests.Session()
        r = sess.post(
            f'{configuration.server_cashless}/api/chargecard',
            headers={
                'Authorization': f'Api-Key {configuration.key_cashless}'
            },
            data=data,
        )

        sess.close()
        logger.info(
            f"        demande au serveur cashless pour {data}. réponse : {r.status_code} ")

        if r.status_code == 202:
            self.ligne_article.status = LigneArticle.VALID
            # set_paiement_and_reservation_valid(None, self.ligne_article)
        else :
            logger.error(
                f"erreur réponse serveur cashless {r.status_code} {r.text}")

    # Categorie ADHESION
    def trigger_A(self):

        logger.info(f"TRIGGER ADHESION")
        logger.info(f"    Envoie celery task.send_membership_to_cashless")
        data = {
            "ligne_article_pk" : self.ligne_article.pk,
        }
        task = send_membership_to_cashless.delay(data)


