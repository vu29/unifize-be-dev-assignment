from decimal import Decimal

from pendulum import datetime

from discounts.base import Discount
from discounts.constants import DiscountType
from discounts.discount_rules.discount_rule_interface import IDiscountRule


class FixedAmountDiscount(Discount):

    def __init__(self, name: str, discount_amount: Decimal, discount_rules: list[IDiscountRule],
                 discount_type: DiscountType, expires_at: datetime, *, discount_code: str | None = None) -> None:
        super().__init__(name, discount_rules, discount_type, expires_at, discount_code=discount_code)
        self.discount_amount = discount_amount

    def calculate_discount_amount(self, current_price: Decimal) -> Decimal:
        """
        Calculate the discount amount based on the current price and the fixed discount amount.
        :param current_price: The current price of the product.
        :return: The discount amount, which is the minimum of the fixed discount amount and the current price.
        """
        return min(self.discount_amount, current_price)
