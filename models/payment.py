from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PaymentMethod(Enum):
    CARD_PAYMENT = "card_payment"
    NET_BANKING = "net_banking"
    UPI = "upi"
    WALLET = "wallet"
    CASH_ON_DELIVERY = "cash_on_delivery"


class CardType(Enum):
    DEBIT_CARD = "debit_card"
    CREDIT_CARD = "credit_card"


@dataclass
class PaymentInfo:
    method: PaymentMethod
    bank_name: Optional[str]
    card_type: Optional[CardType]
