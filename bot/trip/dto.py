import datetime
from dataclasses import dataclass


@dataclass
class TripInfo:
    id: int
    distance: float
    cost: float
    date: datetime.datetime
    auto_identifier: str
    creator_name: str
    number_of_passengers: int
