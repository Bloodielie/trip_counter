from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.trip.models import Fuel


async def get_fuel_by_identifier(session: AsyncSession, identifier: str) -> Optional[Fuel]:
    query = select(Fuel).where(Fuel.identifier == identifier)
    result = await session.execute(query)
    return result.scalars().first()


async def create_fuel(session: AsyncSession, identifier: str, price: Decimal) -> Optional[Fuel]:
    fuel = Fuel(identifier=identifier, price=price)
    session.add(fuel)
    return fuel
