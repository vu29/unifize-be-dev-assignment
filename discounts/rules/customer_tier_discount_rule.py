from discounts.rules.discount_rule_interface import IDiscountRule
from models.cart import CartItem
from models.customer import CustomerProfile, CustomerTier
from models.payment import PaymentInfo


class CustomerTierDiscountRule(IDiscountRule):

    def __init__(self, include_tiers: list[CustomerTier] | None = None,
                 exclude_tiers: list[CustomerTier] | None = None) -> None:
        """
        :param include_tiers: List of customer tiers to include in the discount rule.
        :param exclude_tiers: List of customer tiers to exclude from the discount rule, if any.
        """
        self.include_tiers = include_tiers or []
        self.exclude_tiers = exclude_tiers or []

    def is_applicable(self, *, customer_profile: CustomerProfile, cart_item: CartItem,
                      payment_info: PaymentInfo = None) -> bool:
        customer_tier: CustomerTier = customer_profile.tier
        if self.include_tiers and customer_tier not in self.include_tiers:
            return False
        if self.exclude_tiers and customer_tier in self.exclude_tiers:
            return False
        return True
