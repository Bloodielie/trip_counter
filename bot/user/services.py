from typing import List, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from bot.user.models import User


async def get_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> Optional[User]:
    result = await session.execute(select(User).where(User.telegram_id == tg_id))
    return result.scalars().first()


async def get_users_by_names(session: AsyncSession, names: List[str]) -> List[User]:
    result = await session.execute(select(User).where(User.name.in_(names)))
    return result.scalars().all()


async def get_user_by_name(session: AsyncSession, name: str) -> Optional[User]:
    result = await session.execute(select(User).where(User.name == name))
    return result.scalars().first()
