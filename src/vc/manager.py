from time import sleep
from typing import List

from vc import settings
from vc.soldo.client.client import Soldo


class Singleton(type):
    _instances = None

    def __call__(cls, *args, **kwargs):
        if not cls._instances:
            cls._instances = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances


class SoldoNetworkManger(metaclass=Singleton):
    _network_client = Soldo()

    @classmethod
    def create_wallet(cls, request_timestamp, owner_type, currency, name):
        """ create wallet and add a wallet to the group aff """
        net = cls()
        response_data = net._network_client.create_wallet(request_timestamp, owner_type, currency, name)
        order = response_data.data
        if order.is_valid and order.status == "PLACED":
            sleep(settings.TIME_SLEEP)
            for item in order.items:
                data = net._network_client.add_item_to_group(settings.GROUP_ID, item.id)

        return

    @classmethod
    def user_update(cls, id: int, **kwargs):
        return cls()._network_client.user_update(id, **kwargs)

    @classmethod
    def get_card(cls, card_id: str, showSensitiveData: str = None):
        return cls()._network_client.get_card(card_id, showSensitiveData)

    @classmethod
    def create_card(cls,  request_timestamp, owner_type, owner_public_id,
                    wallet_id, name="aff", emboss_line4=None, type="VIRTUAL", card_label="aff"):
        return cls()._network_client.create_card(
            request_timestamp, owner_type, owner_public_id,
            wallet_id, name=name, emboss_line4=emboss_line4, card_label=card_label, type=type)

    @classmethod
    def create_user(cls, email: str, name: str, surname: str, custom_reference_id: str, job_title: str, **data):
        return cls()._network_client.create_user( email, name, surname=surname, custom_reference_id=custom_reference_id,
                                                  job_title=job_title, **data)
    #
    # @classmethod
    # def set_event(cls, event_name):


        # "https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru"

