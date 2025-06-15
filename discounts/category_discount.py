from typing import List
from decimal import Decimal
from models import CartItem, CustomerProfile, DiscountResult
from discounts.base import Discount


class CategoryDiscount(Discount):
    """Category-specific discount implementation"""
    
    def __init__(self, category: str, discount_percentage: Decimal, max_discount: Decimal):
        self.category = category
        self.discount_percentage = discount_percentage
        self.max_discount = max_discount
    
    def can_apply(self, cart_items: List[CartItem], customer: CustomerProfile) -> bool:
        return any(item.product.category == self.category for item in cart_items)
    
    def apply(self, cart_items: List[CartItem], current_price: Decimal) -> DiscountResult:
        applicable_items = [item for item in cart_items if item.product.category == self.category]
        total_discount = Decimal('0')
        
        for item in applicable_items:
            item_discount = min(
                item.product.base_price * self.discount_percentage / Decimal('100'),
                self.max_discount
            )
            total_discount += item_discount * item.quantity
        
        return DiscountResult(
            discount_amount=total_discount,
            message=f"{self.category} Category Discount: {self.discount_percentage}% off"
        ) 