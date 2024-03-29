import json
import logging
from datetime import datetime
from uuid import UUID, uuid4

import requests
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import localtime

from AuthBillet.models import RsaKey, TibilletUser, Wallet
from BaseBillet.models import Configuration, Membership, Product
from fedow_connect.models import FedowConfig
from fedow_connect.utils import sign_message, data_to_b64, verify_signature
from fedow_connect.validators import WalletValidator, AssetValidator, TransactionValidator

logger = logging.getLogger(__name__)


### GENERIC GET AND POST ###
def _post(fedow_config: FedowConfig = None,
          user: TibilletUser = None,
          data: dict = None,
          path: str = None,
          apikey: str = None):
    fedow_domain = fedow_config.fedow_domain()
    now = f"{datetime.now().isoformat()}"

    # Pour la création, on prend la clé api de Root. On rempli apikey
    # Si vide, on prend la clé du lieu du tenant
    if apikey is None:
        # Pour la création, on prend la clé api de Root. apikey est donné en arguement.
        # Si vide, on prend la clé du lieu du tenant
        apikey = fedow_config.fedow_place_admin_apikey
    headers = {
        "Date": f"{now}",
        'Authorization': f'Api-Key {apikey}',
        "Content-type": "application/json",
    }

    # Si un user est donné, on indique son wallet dans le header et on le signe avec now
    if user:
        # Signature de la requete
        signature = sign_message(
            data_to_b64(data),
            user.get_private_key(),
        ).decode('utf-8')

        # Ici, on s'autovérifie :
        # Assert volontaire. Si non effectué en prod, ce n'est pas grave.
        # logger.debug("_post verify_signature start")
        if not verify_signature(user.get_public_key(),
                                data_to_b64(data),
                                signature):
            raise Exception("Signature auto verification failed")

        headers.update({
            "Wallet": f"{user.wallet.uuid}" if user.wallet else "",
            "Signature": f"{signature}",
        })

    session = requests.Session()
    request_fedow = session.post(
        f"https://{fedow_domain}/{path}/",
        headers=headers,
        data=json.dumps(data),
        verify=bool(not settings.DEBUG),
    )

    # TODO: Vérifier la signature de FEDOW avec root_config.fedow_primary_pub_pem

    session.close()
    return request_fedow


def _get(fedow_config: FedowConfig = None,
         user: TibilletUser = None,
         path: str = None,
         apikey: str = None):
    fedow_domain = fedow_config.fedow_domain()
    now = f"{datetime.now().isoformat()}"

    if apikey is None:
        # Pour la création, on prend la clé api de Root. apikey est donné en arguement.
        # Si vide, on prend la clé du lieu du tenant
        apikey = fedow_config.fedow_place_admin_apikey
    headers = {
        "Date": f"{now}",
        'Authorization': f'Api-Key {apikey}',
    }

    # Si un user est donné, on indique son wallet dans le header et on le signe avec now
    if user:
        # On signe le message
        message = f"{user.wallet.uuid}:{now}"
        signature = sign_message(
            message.encode('utf8'),
            user.get_private_key(),
        ).decode('utf-8')

        # Ici, on s'autovérifie :
        if not verify_signature(user.get_public_key(),
                                message.encode('utf8'),
                                signature):
            raise Exception("Signature auto verification failed")

        headers.update({
            "Wallet": f"{user.wallet.uuid}",
            "Signature": f"{signature}",
        })

    session = requests.Session()
    request_fedow = session.get(
        f"https://{fedow_domain}/{path}/",
        headers=headers,
        verify=bool(not settings.DEBUG),
    )
    session.close()

    # TODO: Vérifier la signature de réponse FEDOW
    return request_fedow


class AssetFedow():
    def __init__(self, fedow_config: FedowConfig or None = None):
        self.fedow_config: FedowConfig = fedow_config
        if fedow_config is None:
            self.fedow_config = FedowConfig.get_solo()

    # def list(self):
    #     response_asset = _get(self.config, ['asset', ])
    #     if response_asset.status_code == 200:
    #         serialized_assets = AssetValidator(data=response_asset.json(), many=True)
    #         if serialized_assets.is_valid():
    #             return serialized_assets.validated_data
    #         logger.error(serialized_assets.errors)
    #         raise Exception(f"{serialized_assets.errors}")

    def retrieve(self, uuid: uuid4 = None):
        response_asset = _get(self.fedow_config, path=f'asset/{UUID(uuid)}/retrieve_membership_asset')

        if response_asset.status_code == 200:
            serialized_assets = AssetValidator(data=response_asset.json(), many=False)
            if serialized_assets.is_valid():
                return serialized_assets.validated_data
            logger.error(serialized_assets.errors)
            raise Exception(f"{serialized_assets.errors}")
        logger.error(response_asset)
        raise Exception(f"{response_asset.status_code}")

    def get_or_create_asset(self, product: Product = None):
        try:
            asset_serialized = self.retrieve(uuid=f"{product.uuid}")
            return asset_serialized, False

        except Exception as e:
            config = Configuration.get_solo()
            asset = {
                "uuid": f"{product.pk}",
                "name": f"{product.name} {config.organisation}",
                "currency_code": f"{product.name[:2]}{product.categorie_article[1:]}".upper(),
                "category": f"{product.fedow_category()}",
                "created_at": timezone.now().isoformat()
            }
            response_asset = _post(self.fedow_config, path='asset/create_membership_asset', data=asset)
            if response_asset.status_code == 201:
                serialized_assets = AssetValidator(data=response_asset.json(), many=False)
                if serialized_assets.is_valid():
                    return serialized_assets.validated_data, True
                logger.error(serialized_assets.errors)
                raise Exception(f"{serialized_assets.errors}")
            logger.error(response_asset)
            raise Exception(f"{response_asset.status_code}")


class MembershipFedow():
    def __init__(self, fedow_config: FedowConfig or None = None):
        self.fedow_config: FedowConfig = fedow_config
        if not fedow_config:
            self.fedow_config = FedowConfig.get_solo()

    def create(self, membership: Membership = None):
        # Si Wallet est None, alors nous en créons ou allons chercher un wallet avec l'email
        if not membership.user.wallet:
            import ipdb;
            ipdb.set_trace()

        # Vérification de l'uuid membership présent coté Fedow
        fedow_asset = AssetFedow(fedow_config=self.fedow_config)
        serialized_asset, created = fedow_asset.get_or_create_asset(membership.price.product)

        user = membership.user
        amount = membership.contribution_value
        sender = self.fedow_config.fedow_place_wallet_uuid
        receiver = user.wallet.uuid
        subscription_start_datetime = membership.last_contribution


        subscription_data = {
            "amount": int(amount * 100),
            "sender": f"{sender}",
            "receiver": f"{receiver}",
            "asset": f"{serialized_asset['uuid']}",
            "subscription_start_datetime": subscription_start_datetime.isoformat(),
        }

        if membership.stripe_paiement.exists():
            subscription_data["metadata"] = {'checkout_session_id_stripe': membership.stripe_paiement.latest('last_action').checkout_session_id_stripe }

        # TODO: Tester lorsqu'on a l'info de la carte
        # if user_card_firstTagId:
        #     subscription['user_card_firstTagId'] = f"{user_card_firstTagId}"
        # if primary_card_fisrtTagId:
        #     subscription['primary_card_fisrtTagId'] = f"{primary_card_fisrtTagId}"

        response_subscription = _post(
            fedow_config=self.fedow_config,
            user=user,
            data=subscription_data,
            path='transaction/create_membership',
        )

        if response_subscription.status_code == 201:
            serialized_transaction = TransactionValidator(data=response_subscription.json())
            if serialized_transaction.is_valid():
                fedow_transaction = serialized_transaction.fedow_transaction
                membership.fedow_transactions.add(fedow_transaction)
                membership.stripe_paiement.latest('last_action').fedow_transactions.add(fedow_transaction)
                return serialized_transaction.validated_data

            logger.error(serialized_transaction.errors)
            return serialized_transaction.errors

        else:
            logger.error(response_subscription.json())
            return response_subscription.status_code

    # def retrieve(self, wallet: uuid4 = None):
    #     response_sub = _get(self.config, ['subscription', f"{UUID(wallet)}"])
    #     if response_sub.status_code == 200:
    #         return response_sub
    #
    #     raise Exception(f"{response_sub.status_code}")


class WalletFedow():
    def __init__(self, fedow_config):
        self.fedow_config: FedowConfig = fedow_config
        if not fedow_config:
            self.fedow_config = FedowConfig.get_solo()

    def retrieve_by_signature(self, user):
        response_link = _get(
            self.fedow_config,
            user=user,
            path=f'wallet/retrieve_by_signature'
        )

        if not response_link.status_code == 200:
            logger.error(f"retrieve_by_signature ERRORS : {response_link.status_code}")
            raise Exception(f"retrieve_by_signature ERRORS : {response_link.status_code}")

        wallet_serialized = WalletValidator(data=response_link.json())
        if wallet_serialized.is_valid():
            return wallet_serialized
        else:
            logger.error(f"retrieve_by_signature wallet_serialized ERRORS : {wallet_serialized.errors}")
            raise Exception(f"retrieve_by_signature wallet_serialized ERRORS : {wallet_serialized.errors}")

    def get_or_create(self, user: TibilletUser):
        email = user.email
        response_link = _post(self.fedow_config, user=user, path='wallet/get_or_create', data={
            "email": email,
            "public_pem": user.get_public_pem(),
        })
        if response_link.status_code in [200, 201]:
            # Création du wallet dans la base de donnée
            if not user.wallet:
                user.wallet, created = Wallet.objects.get_or_create(uuid=UUID(response_link.json()))
                user.save()
            elif user.wallet.uuid != UUID(response_link.json()):
                raise Exception("Wallet and member mismatch")

            created = False if response_link.status_code == 200 else True
            return user.wallet, created

        raise Exception(f"Wallet FedowAPI create_from_email response : {response_link.status_code}")

    def get_federated_token_refill_checkout(self, user: TibilletUser):
        response_checkout = _get(
            self.fedow_config,
            user=user,
            path=f'wallet/get_federated_token_refill_checkout'
        )

        if response_checkout.status_code != 202:
            logger.error(response_checkout.json())
            raise Exception(response_checkout.json())

        stripe_checkout_url = response_checkout.json()
        return stripe_checkout_url


class PlaceFedow():
    def __init__(self, fedow_config):
        self.fedow_config: FedowConfig = fedow_config
        if not fedow_config:
            self.fedow_config = FedowConfig.get_solo()

    def create(self, admin: TibilletUser = None, place_name=None):
        if any([
            self.fedow_config.fedow_place_uuid,
            self.fedow_config.fedow_place_wallet_uuid,
            self.fedow_config.fedow_place_admin_apikey,
        ]):
            raise Exception("Place already created")

        if place_name is None:
            tenant_config = Configuration.get_solo()
            place_name = tenant_config.organisation

        # Pour la création, on prend la clé api de Root
        apikey = self.fedow_config.get_fedow_create_place_apikey()
        data = {
            'place_name': place_name,
            'admin_email': admin.email,
            'admin_pub_pem': admin.get_public_pem(),
        }

        new_place = _post(fedow_config=self.fedow_config,
                          user=admin,
                          path='place',
                          data=data, apikey=apikey)
        new_place_data = new_place.json()
        self.fedow_config.fedow_place_uuid = new_place_data['uuid']
        self.fedow_config.fedow_place_wallet_uuid = new_place_data['wallet']
        self.fedow_config.fedow_place_admin_apikey = new_place_data['key']
        self.fedow_config.save()


class TransactionFedow():
    def __init__(self, fedow_config: FedowConfig or None = None):
        self.fedow_config: FedowConfig = fedow_config
        if fedow_config is None:
            self.config = FedowConfig.get_solo()

    def get_from_hash(self, hash_fedow: str = None):
        response_hash = _get(self.fedow_config, path=f'transaction/{hash_fedow}')
        if response_hash.status_code == 200:
            serialized_transaction = TransactionValidator(data=response_hash.json())
            if serialized_transaction.is_valid():
                validated_data = serialized_transaction.validated_data
                return validated_data
            logger.error(serialized_transaction.errors)
            return serialized_transaction.errors

        else:
            logger.error(response_hash.json())
            return response_hash.status_code

# from fedow_connect.fedow_api import FedowAPI
class FedowAPI():
    def __init__(self, fedow_config: FedowConfig = None):
        self.fedow_config = fedow_config
        if fedow_config is None:
            self.fedow_config = FedowConfig.get_solo()

        self.wallet = WalletFedow(fedow_config=self.fedow_config)
        self.place = PlaceFedow(fedow_config=self.fedow_config)
        self.membership = MembershipFedow(fedow_config=self.fedow_config)
        self.asset = AssetFedow(fedow_config=self.fedow_config)
        self.transaction = TransactionFedow(fedow_config=self.fedow_config)

    def handshake(self):
        pass
