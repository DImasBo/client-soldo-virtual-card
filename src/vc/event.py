

class EventBase(object):
    event_name: str

    def run(self, **data):
        pass


class WalletCreateEvent(EventBase):
    event_name = "wallet_created"
    event_type = "Wallet"

    def run(self, **data):
        pass
        # set model
        # {"id": "bc2a09d0-0bfc-48eb-b596-82bf5f411aef", "name": "WAllet name2 group", "currency_code": "USD",
        #            "available_amount": 0.00, "blocked_amount": 0.00, "primary_user_type": "company", "visible": true,
        #            "creation_time": "2021-06-29T15:44:02Z"}}'