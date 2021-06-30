# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

from vc import settings
from vc.celery_app import celery_app
from vc.manager import SoldoNetworkManger
from vc.soldo.client.requesters import group,card
from vc.soldo.client.requesters.utils import decrypt




def print_hi(name):
    # celery_app.start()

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
    sensitive_data = {
        "encrypted_full_pan": "SLrd4eBzRG6SW5zyjYCpZbztty/KTwiPRxqCjF8uW+ebFN5lMUdmczMrYD5VYFi84yBbun6pH5Tj8uJNKB1Jbnm2AKnriZa+o//zmXQYU/XgtbCcMUHkX5NgoqGpPYOZQRGMjMcVwN5QKpjc6zzz50nqeEEgoAV/fPhdBNUtz0O4omNePkd4ptgrDMmUYKI0hfvo0yTxhpQrsshyQ8agO8eik7vzw9kYDYV/fRDi4KlDj9HfLqH2R9ibiLRL0+Kgk/dai9Zic96qyAO7/TMzyrlqLkWh1YDDbC6MKuLt4v0Y0mS2gZAa47/IyiDBMn5uAz/aeTcKtB0gk4vqmxXA6w==",
        "encrypted_cvv": "UFexqjr5bsRwmfkewjYw5fWD5IV1qFiLLh4e8SNhO955y6CUbQOfhjvx9gD7kgc614uSa/J7LKiz83LukVMllXSiYAyj0ZWH/qkeQ8fE2b0qNqwybIMDJ096ZY0RTB+MMW0LMxQWG1Zr2C+PTQTEvqO+tDuIbMVBB9sg2DrYxTtg3Jzb/TtYMHz+2lKym3ks9qDy55ax1F7rHjQ/KB1X5I5BcoV79q0hPs0G9tNMqaID4X9gVaZ/HxBQOTbetnzcbLd/fsOpjVOTRy7j3jOHpfxbMKMLumX9DhJUK5DPMZTLUh7l9hbzLFnQ+ui21jwJFpThpZVxcVXhuyijzPCCfw=="
    }
    keyPath = settings.PATH_RSA_PRIVATE


    print(decrypt(sensitive_data.get("encrypted_full_pan")))
    print(decrypt(sensitive_data.get("encrypted_cvv")))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
