from sqlalchemy.orm import Session

from vc.client.base import BaseNetworkClient


# from vc.
from .requesters.client_api import user, wallets, card, group, order


from vc.settings import Settings


class Soldo(BaseNetworkClient):

    settings = Settings({
        "ACCESS_TOKEN": "xjn0S9iNN7ZMYbS5g3LxnpsN3ltVPgQX",
    })

    def __init__(self, name, uri,
                 api_url: str,
                 client_id: str,
                 client_secret: str,
                 group_id: str,
                 token: str,
                 filepath_private_pem: str, currency="USD", user_model=None, **config):
        data = dict(name=name, currency = currency,
                                     CLIENT_ID=client_id,
                                     CLIENT_SECRET=client_secret,
                                     API_URL=api_url,
                                     TOKEN=token,
                                     PATH_RSA_PRIVATE=filepath_private_pem,
                                     GROUP_ID = group_id, **config)
        Soldo.settings.update_config(**data)
        super().__init__(uri, user_model=user_model, **config)

    def oauth_authorize(self):
        return user.oauth_authorize()

    def whoami(self):
        return user.whoami()

    def user_update(self, id, **kwargs):
        return user.update(id, **kwargs)

    def create_wallet(self,name, owner_type):
        response_data = wallets.create(owner_type, self.settings.currency, name)
        order = response_data.data
        # if order.is_valid and order.status == "PLACED":
        #     sleep(settings.TIME_SLEEP)
        #     for item in order.items:
        #         data = self.add_item_to_group(settings.GROUP_ID, item.id)
        return response_data

    def create_user(self, db: Session, id: int):
        u = db.query(self._user).filter(self._user.id==id).first()

        response_model = user.create(u.email, u.first_name, u.last_name, u.id, u.job_title)
        if not response_model.data.status == "PLACED" or not response_model.data.is_valid:
            raise ValueError(f"Error create_user {str(response_model.dict())}")
        return u

    def get_card(self, card_id: str, showSensitiveData: str = None):
        return card.get(card_id, showSensitiveData)

    def create_card(self, owner_type, owner_public_id,
                    wallet_id, name, emboss_line4=None, type="VIRTUAL", card_label=None):
        if not card_label:
            card_label = self.settings.name

        return card.create(owner_type=owner_type, owner_public_id=owner_public_id,
                    wallet_id=wallet_id, name=name,
            emboss_line4=emboss_line4,
            type=type,
            card_label=card_label)

    def add_item_to_group(self, groupId: str, id: str, type="WALLET"):
        return group.group_write(groupId, id, type)

    def get_order(self, order_id: str):
        return order.get(order_id)
