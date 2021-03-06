from decimal import Decimal
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from bot.user.models import User


async def get_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_by_tg_id(session: AsyncSession, tg_id: int, is_load_roles: bool = False) -> Optional[User]:
    query = select(User).where(User.telegram_id == tg_id)
    if is_load_roles:
        query = query.options(joinedload(User.roles))

    result = await session.execute(query)
    return result.scalars().first()


async def get_users_by_identifiers(session: AsyncSession, identifiers: List[str]) -> List[User]:
    result = await session.execute(select(User).where(User.identifier.in_(identifiers)))
    return result.scalars().all()


async def get_user_by_identifier(session: AsyncSession, identifier: str) -> Optional[User]:
    result = await session.execute(select(User).where(User.identifier == identifier))
    return result.scalars().first()


async def update_user_balance(session: AsyncSession, user_id: int, amount: Decimal) -> None:
    query = update(User).where(User.id == user_id).values(balance=User.balance + amount)
    await session.execute(query)


async def create_user(session: AsyncSession, telegram_id: int, identifier: str, balance: Decimal = Decimal(0)) -> User:
    user = User(telegram_id=telegram_id, identifier=identifier, balance=balance)
    session.add(user)
    return user
