from datetime import datetime
from enum import Enum
from vc.settings import CLASSBASEMODEL
from sqlalchemy import Column, Integer, ForeignKey, String, Date, DateTime, func, Numeric, Boolean
from sqlalchemy.orm import relationship


class StatusAccountVC(str, Enum):
    deactivated = "Deactivated"
    paid = "Paid"
    beta = "Beta"


class AccountVC(CLASSBASEMODEL):
    __tablename__ = "account_vc"
    number = Column(String(100))
    balance = Column(Numeric, default=0)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(15), default=StatusAccountVC.deactivated.value)
    user = relationship("User", back_populates="accounts")
    campaigns_vc = relationship("CampaignVC", back_populates="account_vc")
    activated_on = Column(DateTime, index=True)
    created_on = Column(DateTime, default=datetime.now, server_default=func.now(), index=True)

    @property
    def is_active(self) -> bool:
        return bool(
            (self.status == StatusAccountVC.beta.value) or (self.status == StatusAccountVC.paid.value))

    def __repr__(self, **kwargs):
        return super().__repr__(f"id: {self.id}| user: {self.user.id}")


class CampaignType(str, Enum):
    # facebook = "facebook"
    # google = "google"
    facebook = "2"
    google = "1"
    prepaidcard = "3"


class CustomStatus(str, Enum):
    hidden = "Hidden"
    not_set = " "


class CampaignVC(CLASSBASEMODEL):
    __tablename__ = "campaign_vc"
    number = Column(String(100))
    balance = Column(Numeric, default=0)
    account_vc_id = Column(Integer, ForeignKey("account_vc.id", ondelete="CASCADE"), index=True, nullable=False)
    account_vc = relationship("AccountVC", back_populates="campaigns_vc")
    type = Column(String, default=CampaignType.facebook.value)
    cards = relationship("CardVC", back_populates="campaign_vc")

    @property
    def count_cards(self):
        return len(self.cards)

    def __repr__(self, **kwargs):
        return super().__repr__(f"id {self.id} type - {self.type}")

    @property
    def sum_cards(self):
        return sum([card.balance for card in self.cards])


class StatusCard(str, Enum):
    pending = "PENDING"
    active = "ACT"
    block = "BLO"
    deleted = "DELETED"


class TypeCard(str, Enum):
    virtual_multi_use = "Virtual multi use"
    single_load_card = "Single load card"


class PaymentSystem(str, Enum):
    master_card = "MASTERCARD"
    visa = "VISA"


class CardVC(CLASSBASEMODEL):
    bin_id = Column(Integer)
    system_id = Column(Integer, index=True)
    reference = Column(String, index=True, unique=True, nullable=False)
    is_slave = Column(Boolean, default=False)
    master_card = relationship("MasterCard", uselist=False ,backref="master_card")

    campaign_vc_id = Column(Integer, ForeignKey("campaign_vc.id", ondelete="CASCADE"))
    campaign_vc = relationship("CampaignVC", back_populates="cards")
    balance = Column(Numeric, default=0)
    PAN = Column(String, index=True)
    cvv = Column(String(5))
    expiry = Column(Date)
    custom_status = Column(String)
    custom_comment = Column(String)
    custom_comment2 = Column(String)
    status = Column(String(20), default=StatusCard.pending.value)
    type = Column(String, default=TypeCard.virtual_multi_use.value)
    payment_system = Column(String, default=PaymentSystem.master_card.value)
    created_on = Column(DateTime, default=datetime.now, server_default=func.now(), index=True)


    def __repr__(self, **kwargs):
        return super().__repr__(f"id {self.id} | PAN: {self.PAN}")
