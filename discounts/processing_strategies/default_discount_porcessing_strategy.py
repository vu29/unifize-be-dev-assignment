from discounts.base import Discount
from discounts.constants import DiscountType
from discounts.processing_strategies.discount_processing_strategy_interface import IDiscountProcessingStrategy


class DefaultDiscountProcessingStrategy(IDiscountProcessingStrategy):
    """
    Default implementation of the discount application strategy.
    Only one discount per category is applied. In case of multiple discounts in the same category,
    one which expires sooner will be applied.
    Discount will be stacked on the base of the discount_type mentioned in `discount_type_ordering`.
    """
    def __init__(self, discount_type_ordering: list[DiscountType]) -> None:
        self.discount_type_ordering = discount_type_ordering

    def resolve_discounts(
            self,
            applicable_discounts: list[Discount],
    ) -> list[Discount]:
        """
        Default strategy that returns all applicable discounts as is.

        :param applicable_discounts: List of discounts to apply.
        :return: The same list of discounts.
        """
        resolved_discounts_list: list[Discount] = []

        discount_type_applied: set[DiscountType] = set()
        applicable_discounts.sort(key=lambda d: d.expires_at)
        for discount in applicable_discounts:
            if discount.discount_type not in discount_type_applied:
                resolved_discounts_list.append(discount)
                discount_type_applied.add(discount.discount_type)

        resolved_discounts_list.sort(
            key=lambda d: self.discount_type_ordering.index(d.discount_type)
        )
        return resolved_discounts_list
