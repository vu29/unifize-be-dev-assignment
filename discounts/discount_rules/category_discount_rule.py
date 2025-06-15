from discounts.discount_rules.discount_rule_interface import IDiscountRule
from models.cart import CartItem
from models.customer import CustomerProfile
from models.payment import PaymentInfo


class CategoryDiscountRule(IDiscountRule):
    def __init__(self, include_categories: list[str] | None = None, exclude_categories: list[str] | None = None) -> None:
        """
        :param include_categories: List of categories to include in the discount rule.
        :param exclude_categories: List of categories to exclude from the discount rule, if any.
        """
        self.include_categories = include_categories or []
        self.exclude_categories = exclude_categories or []

    def is_applicable(self, *, customer_profile: CustomerProfile, cart_item: CartItem, payment_info: PaymentInfo=None) -> bool:
        category_name = cart_item.product.category
        if self.include_categories and category_name not in self.include_categories:
            return False
        if self.exclude_categories and category_name in self.exclude_categories:
            return False
        return True