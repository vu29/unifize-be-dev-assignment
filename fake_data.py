from decimal import Decimal

import pendulum

from discounts.constants import DiscountType
from discounts.percentage_discount import PercentageDiscount
from discounts.rules.brand_discount_rule import BrandDiscountRule
from discounts.rules.category_discount_rule import CategoryDiscountRule
from discounts.rules.payment_discount_rule import PaymentDiscountRule
from models.cart import CartItem
from models.customer import CustomerProfile, CustomerTier
from models.payment import PaymentInfo, PaymentMethod, CardType
from models.product import Product, BrandTier

# Sample Products
PUMA_TSHIRT = Product(
    id="P001",
    brand="PUMA",
    brand_tier=BrandTier.PREMIUM,
    category="T-Shirt",
    base_price=Decimal("2000.00"),
    current_price=Decimal("2000.00")
)

ADIDAS_TSHIRT = Product(
    id="A001",
    brand="ADIDAS",
    brand_tier=BrandTier.PREMIUM,
    category="T-Shirt",
    base_price=Decimal("1800.00"),
    current_price=Decimal("1800.00")
)


# Sample Cart Items
CART_ITEMS = [
    CartItem(
        product=PUMA_TSHIRT,
        quantity=1,
        size="M"
    ),
    CartItem(
        product=ADIDAS_TSHIRT,
        quantity=1,
        size="L"
    )
]


# Sample Customer
CUSTOMER = CustomerProfile(
    id="C001",
    name="John Doe",
    tier=CustomerTier.GOLD,
    email="john@example.com",
    phone="1234567890"
)


# Sample Payment Info
PAYMENT_INFO = PaymentInfo(
    method=PaymentMethod.CARD_PAYMENT,
    bank_name="ICICI Bank",
    card_type=CardType.CREDIT_CARD
)


# Sample Discounts
puma_t_shirt_40_percent_discount = PercentageDiscount(
    name="Puma T-Shirt Discount min 40% off",
    discount_percentage=Decimal(40),
    discount_rules=[
        BrandDiscountRule(include_brands=["PUMA"]),
        CategoryDiscountRule(include_categories=["T-Shirt"]),
    ],
    expires_at= pendulum.DateTime(2025, 12, 31, 23, 59, 59, tzinfo=pendulum.tz.UTC),
    discount_type=DiscountType.BRAND_DISCOUNT
)


additional_10_percent_tshirt_discount = PercentageDiscount(
    name="Additional 10% off T-Shirts",
    discount_percentage=Decimal(10),
    discount_rules=[
        CategoryDiscountRule(include_categories=["T-Shirt"]),
    ],
    expires_at=pendulum.DateTime(2025, 12, 31, 23, 59, 59, tzinfo=pendulum.tz.UTC),
    discount_type=DiscountType.CATEGORY_DISCOUNT
)


icici_bank_10_percent_bank_discount = PercentageDiscount(
    name="ICICI Bank 10% off",
    discount_percentage=Decimal(10),
    discount_rules=[
        PaymentDiscountRule(applicable_banks=["ICICI Bank"]),
    ],
    expires_at=pendulum.DateTime(2025, 12, 31, 23, 59, 59, tzinfo=pendulum.tz.UTC),
    discount_type=DiscountType.BANK_DISCOUNT
)

voucher_discount = PercentageDiscount(
    name="Super 69",
    discount_code="super_69",
    discount_percentage=Decimal(69),
    discount_rules=[],
    expires_at=pendulum.DateTime(2025, 12, 31, 23, 59, 59, tzinfo=pendulum.tz.UTC),
    discount_type=DiscountType.VOUCHER_DISCOUNT
)

DUMMY_DISCOUNTS = [
    puma_t_shirt_40_percent_discount,
    additional_10_percent_tshirt_discount,
    icici_bank_10_percent_bank_discount,
    voucher_discount
]


