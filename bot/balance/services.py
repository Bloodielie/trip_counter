from decimal import Decimal
from typing import List, Tuple

from sqlalchemy import select, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from bot.balance.models import Transaction
from bot.user.models import User


async def get_user_balance(session: AsyncSession, user_id: int) -> Decimal:
    query = select(User.balance).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_all_users_balance(session: AsyncSession) -> List[Tuple[str, Decimal]]:
    query = select([User.identifier, User.balance])
    result = await session.execute(query)
    return result.all()


async def get_user_transactions(
    session: AsyncSession, user: User, limit: int = 50, offset: int = 0
) -> List[Transaction]:
    query = (
        select(Transaction)
        .where(
            Transaction.is_active == True,
            Transaction.id <= offset,
            or_(Transaction.sender == user.id, Transaction.receiver == user.id)
        )
        .order_by(desc(Transaction.id))
        .limit(limit)
        # .offset(offset)
    )
    result = await session.execute(query)
    return result.scalars().all()
