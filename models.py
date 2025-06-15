from dataclasses import dataclass
from typing import List, Optional, Dict
from decimal import Decimal
from enum import Enum


class BrandTier(Enum):
    PREMIUM = "premium"
    REGULAR = "regular"
    BUDGET = "budget"

class CustomerTier(Enum):
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"

class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    NET_BANKING = "net_banking"
    UPI = "upi"
    WALLET = "wallet"
    CASH_ON_DELIVERY = "cash_on_delivery"

class CardType(Enum):
    DEBIT_CARD = "debit_card"
    CREDIT_CARD = "credit_card"

@dataclass
class Product:
    id: str
    brand: str
    brand_tier: BrandTier
    category: str
    base_price: Decimal
    current_price: Decimal


@dataclass
class CartItem:
    product: Product
    quantity: int
    size: str


@dataclass
class PaymentInfo:
    method: PaymentMethod
    bank_name: Optional[str]
    card_type: Optional[CardType]


@dataclass
class CustomerProfile:
    id: str
    name: str
    tier: CustomerTier
    email: str


@dataclass
class DiscountedPrice:
    original_price: Decimal
    final_price: Decimal
    applied_discounts: Dict[str, Decimal]
    message: str


@dataclass
class DiscountResult:
    """Result of applying a discount"""
    discount_amount: Decimal
    message: str 