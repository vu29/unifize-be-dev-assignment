from typing import List
from decimal import Decimal
from models import CartItem, CustomerProfile, DiscountResult
from discounts.base import Discount


class CouponDiscount(Discount):
    """Coupon code discount implementation"""
    
    def __init__(
        self,
        code: str,
        discount_percentage: Decimal,
        max_discount: Decimal,
        min_purchase: Decimal,
        valid_categories: List[str],
        excluded_brands: List[str]
    ):
        self.code = code
        self.discount_percentage = discount_percentage
        self.max_discount = max_discount
        self.min_purchase = min_purchase
        self.valid_categories = valid_categories
        self.excluded_brands = excluded_brands
    
    def can_apply(self, cart_items: List[CartItem], customer: CustomerProfile) -> bool:
        # Check minimum purchase
        cart_total = sum(item.product.base_price * item.quantity for item in cart_items)
        if cart_total < self.min_purchase:
            return False
        
        # Check category restrictions
        cart_categories = {item.product.category for item in cart_items}
        if not cart_categories.issubset(set(self.valid_categories)):
            return False
        
        # Check brand exclusions
        cart_brands = {item.product.brand for item in cart_items}
        if cart_brands.intersection(set(self.excluded_brands)):
            return False
        
        return True
    
    def apply(self, cart_items: List[CartItem], current_price: Decimal) -> DiscountResult:
        discount_amount = min(
            current_price * self.discount_percentage / Decimal('100'),
            self.max_discount
        )
        
        return DiscountResult(
            discount_amount=discount_amount,
            message=f"Coupon Code {self.code}: {self.discount_percentage}% off"
        ) 