from typing import List
from decimal import Decimal
from models import CartItem, CustomerProfile, DiscountResult
from discounts.base import Discount


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