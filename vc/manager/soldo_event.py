from datetime import datetime

from sqlalchemy.orm import Session

from vc.models.soldo import WalletSo


class EventMixer:
    format_date = "%Y-%m-%dT%H:%M:%SZ"

    # events functions

    def new_user(self, db: Session, **data):
        user = db.query(self._user).filter(self._user.email == data.get("email")).first()
        user.soldo_id = data.get("id")
        self.save_obj(db, user)

        if not data.get("groups"):
            self.add_item_to_group(user.soldo_id, type="USER")

        response_data = self.get_wallets(page_size=100)
        wallets = response_data.data.results
        wallets = list(filter(
            lambda w: w.primary_user_public_id == user.soldo_id,
            wallets))

        list_wallet_id = [w.search_id for w in user.wallet_soldo]

        wallets = list(filter(
            lambda w: w.id not in list_wallet_id,
            wallets
        ))

        for w in wallets:
            if w.currency_code in self.settings.currency:
                wallet = WalletSo(
                    user_id=user.id,
                    search_id=w.id,
                    balance=w.available_amount,
                    blocked_balance=w.blocked_amount,
                    currency=w.currency_code)
                if data.get("creation_time"):
                    wallet.created_on = datetime.strptime(data.get("creation_time"), self.format_date)
                self.save_obj(db, wallet)
        return user

    def wallet_created(self, db: Session, **data):
        """2021-07-02 12:56:37,564 - app.api.api_v1.endpoints.utils - DEBUG - b'{"event_type":"Wallet","event_name":"wallet_created",
        "data":
        {"id":"f0dd3007-838b-46e9-899c-3c526c71ee06","name":"test@test.com","currency_code":"USD","available_amount":0.00,"blocked_amount":0.00,"primary_user_type":"company","visible":true,"creation_time":"2021-07-02T09:56:37Z"}}'"""
        user = db.query(self._user).filter(self._user.soldo_id == data.get("primary_user_public_id")).first()

        wallet = WalletSo(
            user_id=user.id,
            search_id=data.get("id"),
            balance=data.get("available_amount"),
            blocked_balance=data.get("blocked_amount"),
            currency=data.get("blocked_amount"),
        )
        if data.get("creation_time"):
            wallet.created_on = datetime.strptime(data.get("creation_time"), self.format_date)
        self.save_obj(db, wallet)

        if not data.get("groups"):
            self.add_item_to_group(wallet.search_id)
        return wallet
