class Settings(object):
    _config = {}

    def __init__(self, conf_dict):
        self._config = conf_dict

    def update_config(self, **kwargs):
        self._config.update(kwargs)

    def __getattr__(self, item):
        if item == "_config":
            return self._config
        # elif item == "update_config":
        #     return self.update_config
        return self._config.get(item)

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, key, value):
        if key == "_config":
            super().__setattr__(key, value)
        else:
            self._config[key] = value

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

# settings = Settings(dict(
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
# ))
