from discounts.discount_rules.discount_rule_interface import IDiscountRule
from models.cart import CartItem
from models.customer import CustomerProfile
from models.payment import PaymentInfo, PaymentMethod


class PaymentDiscountRule(IDiscountRule):

    def __init__(self, applicable_banks: list[str] | None = None,
                 applicable_payment_methods: list[PaymentMethod] | None = None) -> None:
        """
        :param applicable_banks: List of bank names to which this discount rule applies.
        :param applicable_payment_methods: List of payment methods to which this discount rule applies.
        """
        self.applicable_banks = applicable_banks or []
        self.applicable_payment_methods = applicable_payment_methods or []

    def is_applicable(self, *, customer_profile: CustomerProfile, cart_item: CartItem,
                      payment_info: PaymentInfo = None) -> bool:
        if payment_info is None:
            return False

        bank_name: str = payment_info.bank_name
        payment_method: PaymentMethod = payment_info.method

        if self.applicable_banks and bank_name not in self.applicable_banks:
            return False
        if self.applicable_payment_methods and payment_method not in self.applicable_payment_methods:
            return False

        return True
