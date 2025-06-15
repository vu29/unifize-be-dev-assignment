
from abc import ABC, abstractmethod
from decimal import Decimal

import pendulum
from pendulum import datetime

from discounts.constants import DiscountType
from discounts.rules.discount_rule_interface import IDiscountRule
from models.cart import CartItem
from models.customer import CustomerProfile
from models.payment import PaymentInfo


class Discount(ABC):

    def __init__(self, name: str, discount_rules: list[IDiscountRule],
                 discount_type: DiscountType, expires_at: datetime, * , discount_code: str | None = None) -> None:
        self.name = name
        self.discount_rules = discount_rules
        self.discount_type = discount_type
        self.expires_at = expires_at
        self.discount_code = discount_code if discount_code is not None else name

    def is_applicable(self, customer_profile: CustomerProfile, cart_item: CartItem,
                      payment_info: PaymentInfo | None = None) -> bool:
        """
        Check if the discount is applicable to the given product.
        """
        if self.is_expired():
            return False
        for rule in self.discount_rules:
            if not rule.is_applicable(customer_profile=customer_profile, cart_item=cart_item, payment_info=payment_info):
                return False
        return True

    def is_expired(self) -> bool:
        """
        Check if the discount is still valid based on its expiration date.
        """
        return pendulum.now("UTC") >= self.expires_at

    @abstractmethod
    def calculate_discount_amount(self, current_price: Decimal) -> Decimal:
        ...

