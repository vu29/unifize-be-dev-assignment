
class DiscountSystemBaseException(Exception):
    """Base exception for the discount system"""
    pass

class DiscountNotFoundException(DiscountSystemBaseException):
    """Exception raised when a discount is not found."""
    pass

class DiscountExpiredException(DiscountSystemBaseException):
    """Exception raised when a discount has expired."""
    pass