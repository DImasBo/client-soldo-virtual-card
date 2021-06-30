

class BaseNetworkSoldoClient(object):
    def oauth_authorize(self):
        raise NotImplementedError

    def whoami(self):
        raise NotImplementedError

    def user_update(self, id:int, **kwargs):
        raise NotImplementedError

    def create_user(self,email: str, name: str, surname: str, custom_reference_id: str, job_title: str, **data):
        raise NotImplementedError

    def create_wallet(self, request_timestamp, owner_type, currency, name):
        return NotImplementedError

    def create_card(self, request_timestamp, owner_type, owner_public_id,
                    wallet_id, type, name, emboss_line4, card_label="aff"):
        return NotImplementedError

    def add_item_to_group(self, groupId: str, id: str, type="WALLET"):
        return NotImplementedError
