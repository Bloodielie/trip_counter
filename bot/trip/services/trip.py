from decimal import Decimal
from itertools import groupby
from typing import List, Tuple

from sqlalchemy import select, desc, or_, false
from sqlalchemy.ext.asyncio import AsyncSession

from bot.trip.dto import TripInfo
from bot.trip.models import Trip, trip_passengers, Auto
from bot.user.models import User


def get_travel_cost(consumption: float, fuel_price: Decimal, distance: float) -> Decimal:
    consumption_decimal = Decimal(str(consumption))
    distance_decimal = Decimal(str(distance))

    return (consumption_decimal / (100 / distance_decimal)) * fuel_price


def get_travel_cost_for_user(travel_cost: Decimal, users_count: int, multiplier: float) -> Decimal:
    coefficient = (1 / users_count) + (multiplier - 1)
    return travel_cost * Decimal(coefficient)


async def get_user_trips(session: AsyncSession, passenger_id: int, limit: int, offset: int) -> List[Trip]:
    get_user_trip_query = (
        select(
            Trip.id,
            Trip.distance,
            Trip.date,
            Trip.cost,
            Auto.identifier.label("auto_identifier"),
            User.identifier.label("creator_name"),
        )
        .join(trip_passengers, trip_passengers.c.trip == Trip.id)
        .join(Auto, Auto.id == Trip.auto)
        .join(User, User.id == Trip.driver)
        .where(
            Trip.is_deleted == false(),
            Trip.id <= offset,
            or_(trip_passengers.c.passenger == passenger_id, Trip.driver == passenger_id),
        )
        .group_by(Trip.id, Auto.identifier, User.identifier)
        .order_by(desc(Trip.id))
        .limit(limit)
        # .offset(offset)
    )
    result = await session.execute(get_user_trip_query)
    return result.all()


async def get_users_on_user_trips(session: AsyncSession, trips_id: List[int]) -> List[Tuple[int, str]]:
    query = (
        select(Trip.id, User.identifier)
        .join(trip_passengers, Trip.id == trip_passengers.c.trip)
        .join(User, User.id == trip_passengers.c.passenger)
        .where(Trip.is_deleted == false(), Trip.id.in_(trips_id))
    )

    result = await session.execute(query)
    return result.all()


async def get_user_trips_info(session: AsyncSession, user: User, limit: int, offset: int = 0) -> List[TripInfo]:
    trips = await get_user_trips(session, user.id, limit, offset)
    trips_dict = {trip.id: dict(trip) for trip in trips}

    users_in_trips = await get_users_on_user_trips(session, list(trips_dict))
    for trip_id, group_items in groupby(users_in_trips, lambda item: item[0]):
        trips_dict.get(trip_id, {})["passengers"] = [identifier for _, identifier in group_items]

    return [TripInfo(**trip) for trip in trips_dict.values()]
