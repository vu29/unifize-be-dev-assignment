from abc import ABC, abstractmethod

from discounts.base import Discount


class IDiscountProcessingStrategy(ABC):

    @abstractmethod
    def resolve_discounts(
            self,
            applicable_discounts: list[Discount],
    ) -> list[Discount]:
        """
        Resolve and return a list of applicable discounts.
        All discounts returned will be applied in the order they are returned.

        :return: List of applicable discounts.
        """
        ...
