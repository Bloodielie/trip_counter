from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from bot.balance.models import Transaction
from bot.user.models import User


async def get_user_balance(session: AsyncSession, user: User) -> float:
    query = select(func.sum(Transaction.amount)).where(Transaction.user == user.id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_all_users_balance(session: AsyncSession) -> List[Tuple[str, float]]:
    query = (
        select([User.name, func.sum(Transaction.amount)])
        .join(User, User.id == Transaction.user)
        .group_by(Transaction.user)
    )
    result = await session.execute(query)
    return result.all()


async def get_user_transactions(session: AsyncSession, user: User, limit: int = 50) -> List[Transaction]:
    query = select(Transaction).where(Transaction.user == user.id).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()
