from decimal import Decimal

from discounts.base import Discount
from discounts.processing_strategies.discount_processing_strategy_interface import IDiscountProcessingStrategy
from models.cart import CartItem
from models.customer import CustomerProfile
from models.discount import DiscountedPrice
from models.payment import PaymentInfo


class DiscountProcessor:

    def __init__(
            self,
            discount_application_strategy: IDiscountProcessingStrategy
    ) -> None:
        """
        Initialize the DiscountProcessor with a list of discounts.
        """
        self._application_strategy = discount_application_strategy

    def apply_discounts(
            self,
            discounts: list[Discount],
            customer_profile: CustomerProfile,
            cart_items: list[CartItem],
            payment_info: PaymentInfo | None = None
    ) -> DiscountedPrice:
        original_price = Decimal(sum(item.product.base_price for item in cart_items))
        applied_discounts: dict[str, Decimal] = {}
        resolved_discounts: list[Discount] = self._application_strategy.resolve_discounts(discounts)
        message = ""
        for discount in resolved_discounts:
            discount_amount = Decimal(0)
            discount_applied = False
            for item in cart_items:
                if discount.is_applicable(customer_profile=customer_profile, cart_item=item, payment_info=payment_info):
                    discount_applied = True
                    discount_amount += discount.calculate_discount_amount(item.product.current_price)
                    item.product.current_price -= discount_amount
                    applied_discounts[discount.name] = applied_discounts.get(discount.name, Decimal(0)) + discount_amount


            if discount_applied:
                message += f"Applied {discount.name}: {discount_amount} | "
        return DiscountedPrice(
            original_price=original_price,
            final_price=Decimal(sum(item.product.current_price for item in cart_items)),
            applied_discounts=applied_discounts,
            message=message
        )
