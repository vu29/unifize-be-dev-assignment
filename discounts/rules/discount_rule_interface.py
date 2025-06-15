from abc import ABC, abstractmethod

from models.cart import CartItem
from models.customer import CustomerProfile
from models.payment import PaymentInfo


class IDiscountRule(ABC):

    @abstractmethod
    def is_applicable(self, *, customer_profile: CustomerProfile, cart_item: CartItem,
                      payment_info: PaymentInfo | None = None) -> bool:
        """
        Check if the discount rule is applicable.
        This method should be implemented by subclasses to define specific rules.
        """
        ...
