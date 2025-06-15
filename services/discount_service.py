from typing import List, Optional
from decimal import Decimal

from discounts.base import Discount
from exceptions import DiscountNotFoundException, DiscountExpiredException
from models.cart import CartItem
from models.customer import CustomerProfile
from models.discount import DiscountedPrice
from models.payment import PaymentInfo
from repositories.discount_repository import IDiscountRepository


class DiscountService:
    def __init__(self, discount_repository: IDiscountRepository):
        self._discount_repository = discount_repository

    async def calculate_cart_discounts(
        self,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        discount_code: Optional[str] = None
    ) -> DiscountedPrice:
        self.applied_discounts = {}
        original_price = sum(item.product.base_price * item.quantity for item in cart_items)
        current_price = original_price

        # Apply brand and category discounts
        current_price = self._apply_brand_category_discounts(cart_items, customer, current_price)

        # Apply discount code if provided
        if discount_code:
            try:
                current_price = self._apply_discount_code(discount_code, cart_items, customer, current_price)
            except DiscountValidationError as e:
                print(f"Discount code validation failed: {str(e)}")

        # Apply bank offers if payment info is provided
        if payment_info and payment_info.bank_name:
            current_price = self._apply_bank_offers(payment_info, cart_items, customer, current_price)

        return DiscountedPrice(
            original_price=original_price,
            final_price=current_price,
            applied_discounts=self.applied_discounts,
            message=self._generate_discount_message()
        )

    def _apply_brand_category_discounts(
        self,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        current_price: Decimal
    ) -> Decimal:
        """Apply brand and category specific discounts"""
        # Apply brand discounts
        for discount in self.brand_discounts.values():
            if discount.can_apply(cart_items, customer):
                result = discount.apply(cart_items, current_price)
                current_price -= result.discount_amount
                self._add_applied_discount(result.message, result.discount_amount)

        # Apply category discounts
        for discount in self.category_discounts.values():
            if discount.can_apply(cart_items, customer):
                result = discount.apply(cart_items, current_price)
                current_price -= result.discount_amount
                self._add_applied_discount(result.message, result.discount_amount)

        return current_price

    def _apply_discount_code(
        self,
        code: str,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        current_price: Decimal
    ) -> Decimal:
        """Apply discount code if valid"""
        if code not in self.coupon_discounts:
            raise DiscountValidationError(f"Invalid discount code: {code}")

        discount = self.coupon_discounts[code]
        if not discount.can_apply(cart_items, customer):
            raise DiscountValidationError("Discount code cannot be applied to this cart")

        result = discount.apply(cart_items, current_price)
        current_price -= result.discount_amount
        self._add_applied_discount(result.message, result.discount_amount)

        return current_price

    def _apply_bank_offers(
        self,
        payment_info: PaymentInfo,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        current_price: Decimal
    ) -> Decimal:
        """Apply bank-specific offers"""
        if payment_info.bank_name not in self.bank_offers:
            return current_price

        discount = self.bank_offers[payment_info.bank_name]
        if payment_info.card_type not in discount.card_types:
            return current_price

        result = discount.apply(cart_items, current_price)
        current_price -= result.discount_amount
        self._add_applied_discount(result.message, result.discount_amount)

        return current_price

    def _add_applied_discount(self, name: str, amount: Decimal):
        """Add a discount to the applied discounts dictionary"""
        if name in self.applied_discounts:
            self.applied_discounts[name] += amount
        else:
            self.applied_discounts[name] = amount

    def _generate_discount_message(self) -> str:
        """Generate a human-readable message about applied discounts"""
        if not self.applied_discounts:
            return "No discounts applied"

        messages = []
        for name, amount in self.applied_discounts.items():
            messages.append(f"{name}: ₹{amount:.2f} off")

        return " | ".join(messages)

    async def validate_discount_code(
            self,
            code: str,
            cart_items: List[CartItem],
            customer: CustomerProfile
    ) -> bool:
        discount: Discount = await self._discount_repository.get_discount_by_code(code)
        if not discount:
            raise DiscountNotFoundException(f"Discount code '{code}' not found.")
        if discount.is_expired():
            raise DiscountExpiredException(f"Discount code '{code}' has expired.")

        return any(
            discount.is_applicable(customer_profile=customer, cart_item=cart_item) for cart_item in cart_items
        )
