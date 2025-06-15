from abc import ABC, abstractmethod

from discounts.base import Discount


class IDiscountRepository(ABC):

    @abstractmethod
    async def list_all_active_discounts(self) -> list[Discount]:
        """
        List all available discounts.

        :return: A list of all discounts.
        """
        ...

    @abstractmethod
    async def get_discount_by_code(self, discount_id: str) -> Discount | None:
        """
        Get a specific discount by its code.

        :param discount_id: The unique identifier for the discount.
        :return: The discount object if found, otherwise None.
        """
        ...


class InMemoryDiscountRepository(IDiscountRepository):
    """
    In-memory implementation of the discount repository.
    This is a placeholder for actual database or external service integration.
    """

    def __init__(self, discounts: list[Discount] = None):
        self.all_discounts = discounts or []

    async def list_all_active_discounts(self) -> list[Discount]:
        return [discount for discount in self.all_discounts if not discount.is_expired()]

    async def get_discount_by_code(self, discount_code: str) -> Discount | None:
        for discount in self.all_discounts:
            if discount.discount_code == discount_code:
                return discount
        return None
