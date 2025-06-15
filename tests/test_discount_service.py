# Python
from decimal import Decimal
from unittest.mock import AsyncMock

import pendulum
import pytest

from discounts.constants import DiscountType
from discounts.percentage_discount import PercentageDiscount
from discounts.processing_strategies.default_discount_porcessing_strategy import DefaultDiscountProcessingStrategy
from discounts.processor.discount_processor import DiscountProcessor
from discounts.rules.brand_discount_rule import BrandDiscountRule
from exceptions import DiscountNotFoundException
from fake_data import DUMMY_DISCOUNTS
from models.cart import CartItem
from models.customer import CustomerTier, CustomerProfile
from models.discount import DiscountedPrice
from models.payment import PaymentMethod, CardType, PaymentInfo
from models.product import BrandTier, Product
from repositories.discount_repository import InMemoryDiscountRepository
from services.discount_service import DiscountService


@pytest.fixture
def product_factory():
    """Factory for creating product variants."""

    def _create_product(
            brand="Puma",
            brand_tier=BrandTier.PREMIUM,
            category="T-Shirt",
            base_price=1000.0,
            **kwargs
    ):
        return Product(
            id=kwargs.get("id", "prod_123"),
            brand=brand,
            brand_tier=brand_tier,
            category=category,
            base_price=Decimal(base_price),
            current_price=Decimal(kwargs.get("current_price", base_price)),
        )

    return _create_product


@pytest.fixture
def customer_factory():
    """Factory for creating customer variants."""

    def _create_customer(
            tier=CustomerTier.GOLD,
            name="John Doe",
            **kwargs
    ):
        return CustomerProfile(
            id=kwargs.get("id", "cust_123"),
            name=name,
            tier=tier,
            email=kwargs.get("email", "jd@gmail.com"),
            phone=kwargs.get("phone", "1234567890"),
        )

    return _create_customer


@pytest.fixture
def payment_info_factory():
    """Factory for creating payment info variants."""

    def _create_payment_info(
            method=PaymentMethod.CARD_PAYMENT,
            bank_name: str = "ICICI Bank",
            card_type: CardType = CardType.CREDIT_CARD,
            **kwargs
    ):
        return PaymentInfo(
            method=method,
            bank_name=bank_name,
            card_type=kwargs.get("card_type", card_type),
        )

    return _create_payment_info


@pytest.fixture
def discount_service():
    discount_repo = InMemoryDiscountRepository()
    discount_repo.all_discounts = DUMMY_DISCOUNTS

    discount_processor = DiscountProcessor(discount_application_strategy=DefaultDiscountProcessingStrategy(
        [
            DiscountType.BRAND_DISCOUNT,
            DiscountType.CATEGORY_DISCOUNT,
            DiscountType.VOUCHER_DISCOUNT,
            DiscountType.BANK_DISCOUNT,
        ]
    ))

    return DiscountService(
        discount_repository=discount_repo,
        discount_processor=discount_processor
    )


@pytest.mark.asyncio
async def test_calculate_cart_discounts_without_voucher_code(
        product_factory, customer_factory, discount_service, payment_info_factory
):
    puma_tshirt: Product = product_factory(brand="PUMA", category="T-Shirt", base_price=1000.0)
    cart_items: list[CartItem] = [
        CartItem(product=puma_tshirt, quantity=1, size="M")
    ]
    discount_service._discount_repository.list_all_active_discounts = AsyncMock(
        return_value=[PercentageDiscount(
            discount_percentage=Decimal(10),
            discount_rules=[
                BrandDiscountRule(include_brands=["PUMA"]),
            ],
            discount_type=DiscountType.BRAND_DISCOUNT,
            expires_at=pendulum.now("UTC") + pendulum.duration(days=30),
            name="Puma T-Shirt Discount",
        )]
    )

    discounted_price = await discount_service.calculate_cart_discounts(
        cart_items=cart_items,
        customer=customer_factory(),
        payment_info=payment_info_factory(),
    )
    assert isinstance(discounted_price, DiscountedPrice)
    assert isinstance(discounted_price.final_price, Decimal)
    assert isinstance(discounted_price.applied_discounts, dict)

    assert discounted_price.final_price < discounted_price.original_price
    assert discounted_price.final_price == discounted_price.original_price * (100 - Decimal(10)) / Decimal(100)


@pytest.mark.asyncio
async def test_calculate_cart_discounts_invalid_voucher_code(
        discount_service
        , product_factory, customer_factory, payment_info_factory):
    result = await discount_service.calculate_cart_discounts(
        cart_items=[CartItem(product=product_factory(), quantity=1, size="M")],
        customer=customer_factory(),
        payment_info=payment_info_factory(),
        voucher_code="invalid_code",
    )
    assert isinstance(result, DiscountedPrice)
    assert "Invalid voucher code" in result.message

@pytest.mark.asyncio
async def test_validate_discount_code(
        discount_service, product_factory, customer_factory, payment_info_factory
):
    puma_tshirt: Product = product_factory(brand="PUMA", category="T-Shirt", base_price=1000.0)
    cart_items: list[CartItem] = [
        CartItem(product=puma_tshirt, quantity=1, size="M")
    ]

    result = await discount_service.validate_discount_code(
        code="super_69",
        cart_items=cart_items,
        customer=customer_factory(),
    )
    assert result is True

@pytest.mark.asyncio
async def test_validate_discount_code_invalid(
        discount_service, product_factory, customer_factory, payment_info_factory
):
    puma_tshirt: Product = product_factory(brand="PUMA", category="T-Shirt", base_price=1000.0)
    cart_items: list[CartItem] = [
        CartItem(product=puma_tshirt, quantity=1, size="M")
    ]

    with pytest.raises(DiscountNotFoundException):
        await discount_service.validate_discount_code(
            code="invalid_code",
            cart_items=cart_items,
            customer=customer_factory(),
        )

