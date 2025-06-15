from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DiscountedPrice:
    original_price: Decimal
    final_price: Decimal
    applied_discounts: dict[str, Decimal]
    message: str


@dataclass
class DiscountResult:
    """Result of applying a discount"""
    discount_amount: Decimal
    message: str
