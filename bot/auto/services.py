from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.auto.models import Auto


async def get_autos(session: AsyncSession) -> List[Auto]:
    result = await session.execute(select(Auto))
    return result.scalars().all()


async def get_auto_by_identifier(session: AsyncSession, identifier: str) -> Optional[Auto]:
    query = select(Auto).where(Auto.identifier == identifier)
    result = await session.execute(query)
    return result.scalars().first()
