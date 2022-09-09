from vc.client.soldo.client import Soldo
from vc.init_vc import init_virtual_card


def test_implement_network_soldo():
    network: Soldo = init_virtual_card("aff",
                                "soldo",
                                uri=None,
                                celery_broker=None, celery_backend=None, user_model=None,
                                api_url="https://api-demo.soldocloud.net",
                                client_id="<TEST>",
                                client_secret="<TEST>",
                                group_id="<TEST-GROUP>",
                                token="<TOKEN>",
                                filepath_private_pem="rsa_private.pem",
                                )

    assert network.whoami()
