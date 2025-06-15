from abc import ABC, abstractmethod
from typing import List
from decimal import Decimal
from models import CartItem, CustomerProfile, DiscountResult


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