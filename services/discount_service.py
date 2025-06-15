from typing import List, Optional

from discounts.base import Discount
from discounts.constants import DiscountType
from discounts.processor.discount_processor import DiscountProcessor
from exceptions import DiscountNotFoundException, DiscountExpiredException
from models.cart import CartItem
from models.customer import CustomerProfile
from models.discount import DiscountedPrice
from models.payment import PaymentInfo
from repositories.discount_repository import IDiscountRepository


class DiscountService:
    def __init__(self, discount_repository: IDiscountRepository, discount_processor: DiscountProcessor):
        self._discount_repository = discount_repository
        self._discount_processor = discount_processor

    async def calculate_cart_discounts(
            self,
            cart_items: List[CartItem],
            customer: CustomerProfile,
            payment_info: Optional[PaymentInfo] = None,
            voucher_code: Optional[str] = None
    ) -> DiscountedPrice:
        message: str = ""
        active_discounts: list[Discount] = await self._discount_repository.list_all_active_discounts(
            exclude_discount_type={DiscountType.VOUCHER_DISCOUNT})
        if voucher_code:
            voucher_discount: Discount = await self._discount_repository.get_discount_by_code(voucher_code)
            if voucher_discount:
                active_discounts.append(voucher_discount)
            else:
                message = f" Invalid voucher code : {voucher_code} "

        discount_price = self._discount_processor.apply_discounts(customer_profile=customer, cart_items=cart_items,
                                                                  payment_info=payment_info, discounts=active_discounts)
        discount_price.message += message
        return discount_price

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
