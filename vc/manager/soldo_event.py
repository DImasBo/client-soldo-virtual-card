from datetime import datetime

from sqlalchemy.orm import Session

from vc.models.soldo import WalletSo


class EventMixer:
    format_date = "%Y-%m-%dT%H:%M:%SZ"
    # events functions

    def new_user(self, db: Session, **data):
        user = db.query(self._user).filter(self._user.email==data.get("email")).first()
        user.search_id = data.get("id")
        self.save_obj(db, user)
        if not data.get("groups"):
            self.add_item_to_group(user.search_id, type="USER")


        self.create_wallet(db, user.wallet_soldo.id)
        return user

    def wallet_created(self, db: Session, **data):
        """2021-07-02 12:56:37,564 -
        app.api.api_v1.endpoints.utils - DEBUG - b'{"event_type":"Wallet","event_name":"wallet_created",
        "data":
        {"id":"f0dd3007-838b-46e9-899c-3c526c71ee06","name":"test@test.com","currency_code":"USD","available_amount":0.00,"blocked_amount":0.00,"primary_user_type":"company","visible":true,"creation_time":"2021-07-02T09:56:37Z"}}'"""
        user = db.query(self._user).filter(self._user.email==data.get("name")).first()
        wallet = user.wallet_soldo
        wallet.search_id = data.get("id")
        wallet.balance = data.get("available_amount")
        wallet.blocked_balance = data.get("blocked_amount")
        if data.get("creation_time"):
            wallet.created_on = datetime.strptime(data.get("creation_time"), self.format_date)
        self.save_obj(db, wallet)
        if not data.get("groups"):
            self.add_item_to_group(wallet.search_id)
        return wallet
