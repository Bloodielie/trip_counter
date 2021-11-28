from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.trip.dto import AutoParams
from bot.trip.models import Auto, Fuel


async def get_user_autos(session: AsyncSession, user_id: int) -> List[Auto]:
    query = select(Auto).where(Auto.owner == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_auto_by_identifier(session: AsyncSession, identifier: str) -> Optional[Auto]:
    query = select(Auto).where(Auto.identifier == identifier)
    result = await session.execute(query)
    return result.scalars().first()


async def get_auto_params_by_identifier(session: AsyncSession, identifier: str) -> Optional[AutoParams]:
    query = (
        select(Auto.id, Auto.multiplier, Auto.consumption, Fuel.price)
        .join(Fuel, Fuel.id == Auto.fuel)
        .where(Auto.identifier == identifier)
    )
    result = await session.execute(query)
    data = result.first()
    if data is None:
        return None

    return AutoParams(**dict(data))


async def create_auto(
    session: AsyncSession,
    identifier: str,
    multiplier: float,
    consumption: float,
    owner_id: int,
    fuel_id: int
) -> Auto:
    auto = Auto(identifier=identifier, multiplier=multiplier, consumption=consumption, owner=owner_id, fuel=fuel_id)
    session.add(auto)
    return auto
