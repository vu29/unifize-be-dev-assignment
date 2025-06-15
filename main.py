import asyncio
from decimal import Decimal

from discounts.constants import DiscountType
from discounts.processing_strategies.default_discount_porcessing_strategy import DefaultDiscountProcessingStrategy
from discounts.processor.discount_processor import DiscountProcessor
from fake_data import DUMMY_DISCOUNTS, CUSTOMER, PAYMENT_INFO, CART_ITEMS
from models.discount import DiscountedPrice
from repositories.discount_repository import InMemoryDiscountRepository
from services.discount_service import DiscountService


def get_discount_service() -> DiscountService:
    discount_repo = InMemoryDiscountRepository()
    discount_repo.all_discounts = DUMMY_DISCOUNTS

    discount_processor = DiscountProcessor(
        discount_application_strategy=DefaultDiscountProcessingStrategy(
            discount_type_ordering=[
                DiscountType.BRAND_DISCOUNT,
                DiscountType.CATEGORY_DISCOUNT,
                DiscountType.VOUCHER_DISCOUNT,
                DiscountType.BANK_DISCOUNT,
            ]
        ))

    discount_service = DiscountService(
        discount_repository=discount_repo,
        discount_processor=discount_processor
    )
    return discount_service


async def main():
    discount_service = get_discount_service()
    discounted_price : DiscountedPrice = await discount_service.calculate_cart_discounts(cart_items=CART_ITEMS, customer=CUSTOMER,
                                                          payment_info=PAYMENT_INFO)
    print(f"Final Price after discounts: {discounted_price.final_price}")
    print(f"Discount Message: {discounted_price.message}")
    print(f"Discounts Applied: {discounted_price.applied_discounts}")


asyncio.run(main())
