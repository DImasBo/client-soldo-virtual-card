from vc.manager import Soldo
from vc.init_vc import init_virtual_card
from vc.db.base_class import Base

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
# )) PostgresDsn.build(
#       - POSTGRES_SERVER=db
#       - POSTGRES_USER=postgres
#       - POSTGRES_PASSWORD=changethis
#       - POSTGRES_DB=app
#             scheme="postgres",
#             user=values.get("POSTGRES_USER"),
#             password=values.get("POSTGRES_PASSWORD"),
#             host=values.get("POSTGRES_SERVER"),
#             path=f"/{values.get('POSTGRES_DB') or ''}",
#         )
from vc.models.base import UserBase
from vc.models.soldo import WalletSo, CardSo, SoldoBase


def test_create_user(network, email="test@test12.com"):
    with network.get_session() as session:
        user = session.query(network._user).filter(network._user.email == email).first()
        if not user:
            user = network._user(email=email, first_name=email, last_name=email, job_title="job_title")
            network.save_obj(session, user)


def test_card_create(network, email="test@card7.com"):
    print(email)
    test_create_user(network, email)
    # data = input()
    # with network.get_session() as s:
    # network.run_event_db(s, "new_user", **{"id":"FFLX6261-000009","name":"test@card7.com","surname":"test@card7.com","job_title":"job_title","email":"test@card7.com","custom_reference_id":"7","status":"ACTIVE","visible": True,"groups":[],"creation_time":"2021-07-02T12:09:26Z"})

    # data = input()

    # network.run_event_db(s, "wallet_created", **{"id":"ab1661e5-7b12-4585-abe2-60df355e3cee","name":"test@card7.com","currency_code":"USD","available_amount":0.00,"blocked_amount":0.00,"primary_user_type":"company","visible":True,"creation_time":"2021-07-02T12:11:49Z"})

    with network.get_session() as session:
        user = session.query(network._user).filter(network._user.email == email).first()
        print(user)
        wallet = session.query(WalletSo).filter(WalletSo.user_id == user.id).first()
        card = network.create_card(session, wallet.id, "test", type="GOOGLE_CARD", card_label="test card")
        print(card)
        print(card.__dict__)


def test_wallet_create(network, email="test@aff.company"):
    test_create_user(network, email)
    with network.get_session() as session:
        user = session.query(network._user).filter(network._user.email == email).first()
        wallet = network.activate_service(session, user.id)
        print(wallet)
        print(wallet.__dict__)
        return wallet


def print_hi(name):
    network = init_virtual_card("aff",
                                "soldo",
                                uri='postgresql://postgres:changethis@0.0.0.0:5551/app',
                                # uri="postgresql://postgres:changethis@0.0.0.0:5432/app",
                                # uri="postgres://postgres:changethis@0.0.0.0:5432/app",
                                celery_broker=None, celery_backend=None, user_model=UserBase,
                                api_url="https://api-demo.soldocloud.net",
                                client_id="651O44FPEK4LIBECc5Vb0LE3NUZ7dVJ3",
                                client_secret="fd2ORidJ4ACoAjw2F2p0O4bK9V0NEDuX",
                                group_id="24c0dc93-cc1a-47b3-a2e9-686dda2dc975",
                                token="JLG2Z6GNO7DVID6YWF3E",
                                log_file="soldo2.log",
                                safe_wallet="ed7cb872-8d60-4f6b-b386-81db355527d5",
                                safe_user="safe@aff.com",
                                currency="EUR",
                                filepath_private_pem="rsa_private.pem",
                                )

    # print(network.get_transactions())
    SoldoBase.metadata.create_all(network.engine)
    # .metadata.create_all(network.engine)
    # return
    with network.get_session() as s:
        data = network.upload_transaction_wallet(s)
        print(data)
    # with network.get_session() as s:
        # network.internal_transfer(s, 1, 5, 2)
    #     wallets = s.query(WalletSo).all()
    #     list_id = [w.search_id for w in wallets]
    #     for id in list_id:
    #         network.add_item_to_group(id)
    # return
    # test_create_user(network, email="admin.lk@affcountry.com")
    # test_card_create(network, email="admin.lk@affcountry.com")
    # test_wallet_create(network, email="test@company.com")
    # print()

    # with network.get_session() as s:
    #     print(network.upload_cards_full(s))
    #     print(network.upload_wallets(s))
    # test_card_create(network, "test@cardcompany.com")
    # print(network.events)
    # i
    # return
    # with network.get_session() as s:
    #     print(network.get_card_rules(s, 2))
    #     print(network.update_card_rule(s, 2, "MaxPerTx", enabled=True, amount=100))
    #     print(network.get_card_rules(s, 2))
    #     data = {"id": "15706b0e-f1b5-4c37-87bb-1f70bbdc5dc3", "status": "COMPLETED", "creation_time": "2021-07-07T09:21:30",
    #      "last_update_time": "2021-07-07T09:21:34", "is_valid": True, "total_paid_amount": 1.000000,
    #      "total_paid_currency": "EUR",
    #      "items": [{"id": "d9901038-32b1-49c9-bcca-c546dbfad5f6", "itemType": "GOOGLE_CARD", "category": "CARD"}]}
    #     network.update_cache(**{'15706b0e-f1b5-4c37-87bb-1f70bbdc5dc3':
    #                               {'wallet_id': 1, 'status': 'PLACED', 'category': 'CARD'}})
    #     print(network.get_cache())
    #     network.run_event_db(s, "store_order_completed", **data)
    #
    #     print(network.get_cache())

        # data = {"id": "e988af25-d4db-4ce3-8f77-3f53894d9284", "name": "test@test121212.com", "currency_code": "EUR",
        #         "available_amount": 0.00, "blocked_amount": 0.00, "primary_user_type": "company", "visible": True,
        #         "creation_time": "2021-07-05T16:12:27Z"}
        # network.run_event_db(s, "wallet_created", **data)
        # self.__cache =
    #     network.__cache = {
    #         'c274b136-5999-4626-850c-46f5db5e5473': {'id': '1d4df4f9-0c89-4913-8d68-8e6c9d19c611', 'wallet_id': 1,
    #                                                  'status': 'PLACED', 'category': 'CARD'},
    #         '13301179-938f-41b6-8193-9021c4149819': {'wallet_id': 4, 'status': 'PLACED', 'category': 'CARD'}}
    #     data = {"id": "c274b136-5999-4626-850c-46f5db5e5473", "status": "COMPLETED",
    #             "creation_time": "2021-07-03T16:53:30", "last_update_time": "2021-07-03T16:53:34", "is_valid": True,
    #             "total_paid_amount": 1.000000, "total_paid_currency": "EUR",
    #             "items": [{"id": "1d4df4f9-0c89-4913-8d68-8e6c9d19c611", "itemType": "VIRTUAL", "category": "CARD"}]}

    # data = {"id": "FFLX6261-000021", "name": "test@222gmail2.com", "surname": "test@222gmail2.com",
    #           "job_title": "job_title", "email": "test@222gmail2.com", "custom_reference_id": "4",
    #           "status": "ACTIVE", "visible": True, "groups": [], "creation_time": "2021-07-05T12:25:22Z"}
    # network.run_event_db(s, event_name="new_user", **data)
    # #     # data = {"id":"FFLX6261-000010","name":"test@test12.com","surname":"test@test12.com","job_title":"job_title","email":"test@test12.com","custom_reference_id":"9","status":"ACTIVE","visible": True,"groups":[],"creation_time":"2021-07-02T13:04:40Z"}
    #     data = {"id":"FFLX6261-000011","name":"test@bug.com","surname":"test@bug.com","job_title":"job_title","email":"test@bug.com","custom_reference_id":"10","status":"ACTIVE","visible":True,"groups":[],"creation_time":"2021-07-02T13:33:39Z"}
    #     data =primary_user_public_id
    #     data ={"id":"FFLX6261-000015","name":"test@soldo.com","surname":"test@soldo.com","job_title":"job_title","email":"test@soldo.com","custom_reference_id":"1","status":"ACTIVE","visible":True,"groups":[],"creation_time":"2021-07-02T14:40:22Z"}
    #     data = {"id":"FFLX6261-000015","name":"test@soldo.com","surname":"test@soldo.com","job_title":"job_title","email":"test@soldo.com","custom_reference_id":"1","status":"ACTIVE","visible":True,"groups":[],"creation_time":"2021-07-02T14:40:22Z"}
    #     data = {"id":"FFLX6261-000016","name":"test@322323.com","surname":"test@322323.com","job_title":"job_title","email":"test@322323.com","custom_reference_id":"2","status":"ACTIVE","visible":True,"groups":[],"creation_time":"2021-07-02T15:54:21Z"}
    #     data = {"id":"FFLX6261-000017","name":"test@2gmail.com","surname":"test@2gmail.com","job_title":"job_title","email":"test@2gmail.com","custom_reference_id":"2","status":"ACTIVE","visible":True,"groups":[],"creation_time":"2021-07-03T16:33:26Z"}
    #     network.run_event_db(s, "new_user", **data)
    # network.run_eve":"test@test12.com","surname":"test@test12.com","job_title":"job_title","email":"test@test12.com","custom_reference_id":"9","status":"ACTIVE","visible": True,"groups":[],"creation_time":"2021-07-02T13:04:40Z"}
    #     data = {"id":"FFLX6261-000011","name":"nt_db(s, "new_user", **data)
    # data ={"id":"65c81c18-39c5-4fe6-bdac-a53ccbe24d26","name":"test@test12.com","currency_code":"USD","available_amount":0.00,"blocked_amount":0.00,"primary_user_type":"company","visible":True,"creation_time":"2021-07-02T13:08:21Z"}
    # network.run_event_db(s, "wallet_created", **data)
    # network.run_event_db(s, "wallet_created", **{"id":"f0dd3007-838b-46e9-899c-3c526c71ee06","name":"test@test.com","currency_code":"USD","available_amount":0.00,"blocked_amount":0.00,"primary_user_type":"company","visible": True,"creation_time":"2021-07-02T09:56:37Z"})
    # network.run_event_db(s, "wallet_created", **{"id":"1451cf6e-ec94-4800-b86a-5be5cedce316","name":"test@card3.com test@card3.com","currency_code":"EUR","available_amount":0.00,"blocked_amount":0.00,"primary_user_type":"employee","primary_user_public_id":"FFLX6261-000006","custom_reference_id":"4","visible":True,"creation_time":"2021-07-02T11:35:38Z"})
    # data = {"id":"3ecdf6f8-4bd5-4e88-b2c6-459f6045511c","status":"COMPLETED","creation_time":"2021-07-04T10:41:16","last_update_time":"2021-07-04T10:41:20", "is_valid": True,"total_paid_amount":1.000000,"total_paid_currency":"EUR","items":[{"id":"48ea65aa-d41e-4349-ae4d-c79b6a1966d8","itemType":"VIRTUAL","category":"CARD"}]}
    # data = {"id":"c274b136-5999-4626-850c-46f5db5e5473","status":"COMPLETED","creation_time":"2021-07-03T16:53:30","last_update_time":"2021-07-03T16:53:34","is_valid": True,"total_paid_amount":1.000000,"total_paid_currency":"EUR","items":[{"id":"1d4df4f9-0c89-4913-8d68-8e6c9d19c611","itemType":"VIRTUAL","category":"CARD"}]}
    # network.run_event_db(s, "store_order_completed", **data)
    # print(network.get_card("f5b083f0-f9ca-473d-8885-8f5aa8697422", showSensitiveData=True))
    # print(network.get_card("f5b083f0-f9ca-473d-8885-8f5aa869742", showSensitiveData=True))
    # print(network.create_user(email="test@test.com", name="name", surname="surname", job_title="title"))

    # Use a breakpoint in the code line below to debug your script.
    # data = SoldoNetworkManger.oauth_authorize()
    # print(f'Hi, {data}')  # Press Ctrl+F8 to toggle the breakpoint.

    # print(SoldoNetworkManger.create_wallet(int(time.time()), "company", "USD", "WAllet name2 group"))
    # print(group.group_write("5eaf2676-4912-4a2f-92bf-d24f58323dbe", "87d95150-41f3-46a5-9501-ca1b368696ca"))
    # print(SoldoNetworkManger.create_card(
    #     int(time.time()), "employee", "FFLX6261-000004", "a60525c8-ff55-4827-b70a-f1f620baf94a",
    # ))
    # print(SoldoNetworkManger.get_card("f5b083f0-f9ca-473d-8885-8f5aa8697422", "true"))
    # , , owner_public_id,
    # wallet_id, type, name, emboss_line4, card_label)
    # print(SoldoNetworkManger.create_user(
    #     **{
    #     "email": "test@mail.com",
    #     "request_timestamp": 1576850500000,
    #   "name": "aname",
    #   "middlename": "amiddlename",
    #   "surname": "asurname",
    #   "dob": "1977-01-01",
    #   "job_title": "Boss",
    #   "custom_reference_id": "acustomreference",
    #   "mobile": "12345678",
    #   "mobile_prefix": "+44",
    #   "mobile_access": False,
    #   "web_access": True}))
    #     # email="email@gmail.com", name="name", surname="surname",
    #     # custom_reference_id="1",
    #     # job_title="title")
    # sensitive_data = {
    #     "encrypted_full_pan": "SLrd4eBzRG6SW5zyjYCpZbztty/KTwiPRxqCjF8uW+ebFN5lMUdmczMrYD5VYFi84yBbun6pH5Tj8uJNKB1Jbnm2AKnriZa+o//zmXQYU/XgtbCcMUHkX5NgoqGpPYOZQRGMjMcVwN5QKpjc6zzz50nqeEEgoAV/fPhdBNUtz0O4omNePkd4ptgrDMmUYKI0hfvo0yTxhpQrsshyQ8agO8eik7vzw9kYDYV/fRDi4KlDj9HfLqH2R9ibiLRL0+Kgk/dai9Zic96qyAO7/TMzyrlqLkWh1YDDbC6MKuLt4v0Y0mS2gZAa47/IyiDBMn5uAz/aeTcKtB0gk4vqmxXA6w==",
    #     "encrypted_cvv": "UFexqjr5bsRwmfkewjYw5fWD5IV1qFiLLh4e8SNhO955y6CUbQOfhjvx9gD7kgc614uSa/J7LKiz83LukVMllXSiYAyj0ZWH/qkeQ8fE2b0qNqwybIMDJ096ZY0RTB+MMW0LMxQWG1Zr2C+PTQTEvqO+tDuIbMVBB9sg2DrYxTtg3Jzb/TtYMHz+2lKym3ks9qDy55ax1F7rHjQ/KB1X5I5BcoV79q0hPs0G9tNMqaID4X9gVaZ/HxBQOTbetnzcbLd/fsOpjVOTRy7j3jOHpfxbMKMLumX9DhJUK5DPMZTLUh7l9hbzLFnQ+ui21jwJFpThpZVxcVXhuyijzPCCfw=="
    # }
    # keyPath = settings.PATH_RSA_PRIVATE
    #
    #
    # print(decrypt(sensitive_data.get("encrypted_full_pan")))
    # print(decrypt(sensitive_data.get("encrypted_cvv")))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
