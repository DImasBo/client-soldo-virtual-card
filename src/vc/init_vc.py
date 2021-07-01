#     API_URL = "https://api-demo.soldocloud.net",
#     CLASSBASEMODEL = None,
#     CLIENT_ID = "651O44FPEK4LIBECc5Vb0LE3NUZ7dVJ3",
#     CLIENT_SECRET = "fd2ORidJ4ACoAjw2F2p0O4bK9V0NEDuX",
#     ACCESS_TOKEN = "PvwlalZvYk1098Lh1gq7AgeKARun8nMP",
#     TOKEN = "JLG2Z6GNO7DVID6YWF3E",
#     CURRENCY="USD",
#     GROUP_ID = "408bf905-3457-4108-aedb-53c88fe9d154",
#     TIME_SLEEP = 3,
#     PATH_RSA_PRIVATE = "rsa_private.pem",
#     CELERY_BROKER_URL=None,
#     CELERY_BACKEND=None,

def init_virtual_card(name:str, service: str,
                      uri: str,
                      celery_broker: str,
                      celery_backend: str,
                      user_model,
                      **config):
    from vc.client.soldo.client import Soldo
    required_config = []
    network = None
    if "soldo" == service:
        # required_config = ["api_url", "client_id", "client_secret", "group_id", "token", "filepath_private_pem"]
        network = Soldo

    # for item in required_config:
    #     if not config.get(item):
    #         return ValueError(f"{item} is required")

    return network(name, uri=uri, celery_broker=celery_broker, user_model=user_model, celery_backend=celery_backend,
                   **config)