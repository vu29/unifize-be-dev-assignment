from discounts.rules.discount_rule_interface import IDiscountRule
from models.cart import CartItem
from models.customer import CustomerProfile
from models.payment import PaymentInfo


class BrandDiscountRule(IDiscountRule):

    def __init__(self, include_brands: list[str] | None = None, exclude_brands: list[str] | None = None) -> None:
        """
        :param include_brands: List of brands to include in the discount rule.
        :param exclude_brands: List of brands to exclude from the discount rule.
        """
        self.include_brands = include_brands or []
        self.exclude_brands = exclude_brands or []


    def is_applicable(self, *, customer_profile: CustomerProfile, cart_item: CartItem,
                      payment_info: PaymentInfo | None = None) -> bool:
        brand_name = cart_item.product.brand
        if self.include_brands and brand_name not in self.include_brands:
            return False
        if self.exclude_brands and brand_name in self.exclude_brands:
            return False
        return True
