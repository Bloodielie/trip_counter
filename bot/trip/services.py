from typing import List

from sqlalchemy import select, LABEL_STYLE_TABLENAME_PLUS_COL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from bot.auto.models import Auto
from bot.trip.dto import TripInfo
from bot.trip.models import Trip, trips_users
from bot.user.models import User


def get_travel_cost(auto: Auto, distance: float) -> float:
    return (auto.consumption / (100 / distance) * auto.fuel_price) * auto.multiplier


async def get_user_trips(session: AsyncSession, user: User, limit: int = 50) -> List[TripInfo]:
    number_of_passengers = select(func.count(trips_users.c.user)).where(trips_users.c.trip == Trip.id).correlate(Trip)
    query = (
        select(
            Trip.id,
            Trip.distance,
            Trip.date,
            Trip.cost,
            Auto.identifier.label("auto_identifier"),
            User.name.label("creator_name"),
            number_of_passengers.label("number_of_passengers"),
        )
        .join(trips_users, trips_users.c.trip == Trip.id)
        .join(Auto, Auto.id == Trip.auto)
        .join(User, User.id == Trip.creator)
        .where(trips_users.c.user == user.id)
        .limit(limit)
    )

    result = await session.execute(query)
    return [TripInfo(**dict(trip)) for trip in result]
