from dataclasses import dataclass
from enum import Enum


class CustomerTier(Enum):
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"


@dataclass
class CustomerProfile:
    id: str
    name: str
    tier: CustomerTier
    email: str
