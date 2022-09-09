from vc.client.soldo import user, card
from vc.client.soldo.requesters.schemas import CardResponse, ListRules

TEST_CARD_ID = "f5b083f0-f9ca-473d-8885-8f5aa8697422"

def test_user_client_whoami():
    assert user.whoami()


def test_card_client_get():
    resource = card.get(TEST_CARD_ID, showSensitiveData=True)
    assert isinstance(resource.data, CardResponse)

def test_card_client_get_rule():
    resource = card.get_card_rules(TEST_CARD_ID)
    assert isinstance(resource.data, ListRules)
    assert len(resource.data.rules) > 0



