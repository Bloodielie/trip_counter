import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class TripInfo:
    id: int
    distance: float
    cost: float
    date: datetime.datetime
    auto_identifier: str
    creator_name: str
    passengers: List[str]


@dataclass
class AutoParams:
    id: int
    multiplier: float
    consumption: float
    price: Decimal
