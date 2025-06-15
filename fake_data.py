from decimal import Decimal

from models import Product, BrandTier, CartItem, CustomerProfile, CustomerTier, PaymentInfo, PaymentMethod, CardType

# Sample Products
PUMA_TSHIRT = Product(
    id="P001",
    brand="PUMA",
    brand_tier=BrandTier.PREMIUM,
    category="T-shirts",
    base_price=Decimal("2000.00"),
    current_price=Decimal("2000.00")
)

ADIDAS_TSHIRT = Product(
    id="A001",
    brand="ADIDAS",
    brand_tier=BrandTier.PREMIUM,
    category="T-shirts",
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
    email="john@example.com"
)

# Sample Payment Info
PAYMENT_INFO = PaymentInfo(
    method=PaymentMethod.CREDIT_CARD,
    bank_name="ICICI",
    card_type=CardType.CREDIT_CARD
)

# Sample Discount Codes
DISCOUNT_CODES = {
    "SUPER69": {
        "discount_percentage": Decimal("69.00"),
        "min_purchase": Decimal("1000.00"),
        "max_discount": Decimal("2000.00"),
        "valid_categories": ["T-shirts", "Jeans", "Shoes"],
        "excluded_brands": ["GUCCI", "PRADA"]
    },
    "WELCOME50": {
        "discount_percentage": Decimal("50.00"),
        "min_purchase": Decimal("500.00"),
        "max_discount": Decimal("1000.00"),
        "valid_categories": ["T-shirts"],
        "excluded_brands": []
    }
}

# Brand Discounts
BRAND_DISCOUNTS = {
    "PUMA": {
        "discount_percentage": Decimal("40.00"),
        "min_purchase": Decimal("1000.00"),
        "max_discount": Decimal("5000.00")
    }
}

# Category Discounts
CATEGORY_DISCOUNTS = {
    "T-shirts": {
        "discount_percentage": Decimal("10.00"),
        "min_purchase": Decimal("500.00"),
        "max_discount": Decimal("2000.00")
    }
}

# Bank Offers
BANK_OFFERS = {
    "ICICI": {
        "discount_percentage": Decimal("10.00"),
        "min_purchase": Decimal("1000.00"),
        "max_discount": Decimal("2000.00"),
        "card_types": ["CREDIT", "DEBIT"]
    }
}