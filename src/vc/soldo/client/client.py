from vc.soldo.base import BaseNetworkSoldoClient


# from vc.
from vc.soldo.client.requesters import user, wallets, card, group, order


class Soldo(BaseNetworkSoldoClient):

    def oauth_authorize(self):
        return user.oauth_authorize()

    def whoami(self):
        return user.whoami()

    def user_update(self, id, **kwargs):
        return user.update(id, **kwargs)

    def create_wallet(self, request_timestamp, owner_type, currency, name):
        return wallets.create(request_timestamp, owner_type, currency, name)

    def create_user(self, email: str, name: str, surname: str, custom_reference_id: str, job_title: str, **data):
        return user.create(email, name, surname, custom_reference_id, job_title, **data)

    def get_card(self, card_id: str, showSensitiveData: str = None):
        return card.get(card_id, showSensitiveData)

    def create_card(self, request_timestamp, owner_type, owner_public_id,
                    wallet_id, name, emboss_line4=None, type="VIRTUAL", card_label="aff"):
        return card.create(
            request_timestamp, owner_type=owner_type, owner_public_id=owner_public_id,
                    wallet_id=wallet_id, name=name,
            emboss_line4=emboss_line4, type=type, card_label=card_label)

    def add_item_to_group(self, groupId: str, id: str, type="WALLET"):
        return group.group_write(groupId, id, type)

    def get_order(self, order_id: str):
        return order.get(order_id)
