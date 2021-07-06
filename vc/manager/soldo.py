import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from sqlalchemy.orm import Session

from .base import BaseNetworkClient

# from vc.
from vc.client.soldo import user, wallets, card, group, order
from vc.models.soldo import WalletSo, CardSo, SoldoStatusToSystem
from vc.settings import Settings
from .soldo_event import EventMixer
from vc.libs.utils import set_config

logger = logging.getLogger(__name__)
set_config(logger, filename="soldo2.log")


class SoldoException(Exception):

    def __init__(self, msg: str, response_data: dict):
        self.msg = msg
        self.response_data = response_data

    def __str__(self):
        return f"{self.msg}, {str(self.response_data)}"


class Soldo(EventMixer, BaseNetworkClient):
    settings = Settings({
        "ACCESS_TOKEN": "T9Yudxf8ZixZ4Gl5mGlzbdJg8GT6zdcJ",
    })
    event_list = ["new_user", "wallet_created", "store_order_completed"]
    __cache = {'c274b136-5999-4626-850c-46f5db5e5473':
                   {"id": "1d4df4f9-0c89-4913-8d68-8e6c9d19c611", 'wallet_id': 1, 'status': 'PLACED',
                    "category": "CARD"}, }

    def get_cache(self, key: str):
        return self.__cache.get(key)

    def __init__(self, name, uri,
                 api_url: str,
                 client_id: str,
                 client_secret: str,
                 group_id: str,
                 token: str,
                 wallet_safe: str,
                 filepath_private_pem: str, log_file: str = None, currency="USD", user_model=None, **config):
        data = dict(name=name, currency=currency,
                    CLIENT_ID=client_id,
                    CLIENT_SECRET=client_secret,
                    API_URL=api_url,
                    TOKEN=token,
                    WALLET_SAFE=wallet_safe,
                    USER_MODEL=user_model,
                    LOG_FILE=log_file,
                    PATH_RSA_PRIVATE=filepath_private_pem,
                    GROUP_ID=group_id, **config)
        set_config(logger, filename=Soldo.settings.LOG_FILE)
        Soldo.settings.update_config(**data)
        super().__init__(uri, user_model=user_model, **config)

    def activate_service(self, db: Session, user_id: int, owner_type="company"):
        user = db.query(self._user).filter(self._user.id == user_id).first()
        logger.debug(user.__dict__)
        response_data = wallets.create(owner_type, self.settings.currency, name=user.email, custom_reference_id=user.id)
        order = response_data.data
        if not order.is_valid or order.status != "PLACED":
            raise SoldoException("Error create_wallet", response_data.dict())

        wallet = WalletSo(user_id=user.id, currency=self.settings.currency, )
        if order.items:
            wallet.search_id = order.items[0].id

        self.save_obj(db, wallet)
        return wallet

    def upload_wallets(self, db: Session):
        response_wallets = wallets.search(page_size=1000500, type="company").data.results
        query_wallets = db.query(WalletSo).filter(WalletSo.search_id is not None).all()

        list_wallets_id = []
        list_wallets = []
        for w in query_wallets:
            list_wallets_id.append(w.search_id)
            list_wallets.append({"search_id": w.search_id, "id": w.id})

        filter_wallet = list(filter(
            lambda w: w.id in list_wallets_id,
            response_wallets
        ))
        update_wallets = []
        for wallet in filter_wallet:
            response_wallet = list(filter(
                lambda w: w.get("search_id") == wallet.id ,
                list_wallets
            ))
            if response_wallet:
                update_wallets.append({
                    "id": response_wallet[0].get("id"),
                    "balance": wallet.available_amount,
                    "blocked_balance": wallet.blocked_amount
                })

        db.bulk_update_mappings(WalletSo, update_wallets)
        db.commit()
        return update_wallets

    def wallet_update_balance(self, db: Session, wallet_id: int):
        wallet = db.query(WalletSo).filter(WalletSo.id == wallet_id).first()
        response_data = wallets.get(wallet.search_id)
        wallet.balance = response_data.data.available_amount
        wallet.blocked_balance = response_data.data.blocked_amount
        self.save_obj(db, wallet)
        return wallet

    def get_wallets(self, **kwargs):
        response_data = wallets.search(**kwargs)
        print(response_data)
        return response_data

    def get_card(self, card_id: str = None, showSensitiveData: str = None, **kwargs):
        return card.get(card_id, showSensitiveData)

    def update_info_card(self, db: Session, id: int, showSensitiveData=True):
        card_obj = db.query(CardSo).filter(CardSo.id == id).first()
        response_data = card.get(card_obj.search_id, showSensitiveData)
        response_card = response_data.data
        card_obj.PAN = response_card.pan
        card_obj.cvv = response_card.cvv
        card_obj.type = response_card.type
        card_obj.created_on = response_card.creation_time
        card_obj.expiry = response_card.expiration_date.date()
        card_obj.PAN = response_card.pan
        card_obj.status = SoldoStatusToSystem.validate(response_card.status)
        self.save_obj(db, card_obj)
        return card_obj

    def create_card(self, db: Session, user_id: int,
                    name: str = None, emboss_line4: str = None, type="VIRTUAL", card_label=None):
        wallet = db.query(WalletSo).filter(WalletSo.user_id == user_id).first()
        user = wallet.user

        if not card_label:
            card_label = self.settings.name

        if not name:
            name = user.email

        response_data = card.create(
            owner_public_id=wallet.search_id,
            wallet_id=wallet.search_id,
            name=name,
            emboss_line4=emboss_line4,
            type=type,
            card_label=card_label)
        order = response_data.data

        if not order.is_valid or order.status != "PLACED":
            raise SoldoException("Error create_card", response_data.dict())
        result = {
            "wallet_id": wallet.id,
            "status": order.status,
            "category": "CARD"
        }
        self.__cache[order.id] = result
        return result

    def add_item_to_group(self, id: str, type="WALLET", groupId: str = None):
        if not groupId:
            groupId = self.settings.GROUP_ID
        return group.group_write(groupId, id, type)

    def get_order(self, order_id: str):
        return order.get(order_id)
