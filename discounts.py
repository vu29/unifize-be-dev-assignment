from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict
from decimal import Decimal
from fake_data import CartItem, CustomerProfile, PaymentInfo


@dataclass
class DiscountResult:
    """Result of applying a discount"""
    discount_amount: Decimal
    message: str


class Discount(ABC):
    """Base interface for all discount types"""
    
    @abstractmethod
    def can_apply(self, cart_items: List[CartItem], customer: CustomerProfile) -> bool:
        """Check if this discount can be applied"""
        pass
    
    @abstractmethod
    def apply(self, cart_items: List[CartItem], current_price: Decimal) -> DiscountResult:
        """Apply the discount and return the result"""
        pass


class BrandDiscount(Discount):
    """Brand-specific discount implementation"""
    
    def __init__(self, brand: str, discount_percentage: Decimal, max_discount: Decimal):
        self.brand = brand
        self.discount_percentage = discount_percentage
        self.max_discount = max_discount
    
    def can_apply(self, cart_items: List[CartItem], customer: CustomerProfile) -> bool:
        return any(item.product.brand == self.brand for item in cart_items)
    
    def apply(self, cart_items: List[CartItem], current_price: Decimal) -> DiscountResult:
        applicable_items = [item for item in cart_items if item.product.brand == self.brand]
        total_discount = Decimal('0')
        
        for item in applicable_items:
            item_discount = min(
                item.product.base_price * self.discount_percentage / Decimal('100'),
                self.max_discount
            )
            total_discount += item_discount * item.quantity
        
        return DiscountResult(
            discount_amount=total_discount,
            message=f"{self.brand} Brand Discount: {self.discount_percentage}% off"
        )


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


class BankOfferDiscount(Discount):
    """Bank-specific offer implementation"""
    
    def __init__(self, bank_name: str, discount_percentage: Decimal, max_discount: Decimal, card_types: List[str]):
        self.bank_name = bank_name
        self.discount_percentage = discount_percentage
        self.max_discount = max_discount
        self.card_types = card_types
    
    def can_apply(self, cart_items: List[CartItem], customer: CustomerProfile) -> bool:
        return True  # Bank offers are checked separately with payment info
    
    def apply(self, cart_items: List[CartItem], current_price: Decimal) -> DiscountResult:
        discount_amount = min(
            current_price * self.discount_percentage / Decimal('100'),
            self.max_discount
        )
        
        return DiscountResult(
            discount_amount=discount_amount,
            message=f"{self.bank_name} Bank Offer: {self.discount_percentage}% off"
        )


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