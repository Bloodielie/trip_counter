from typing import Optional

from aiogram import Dispatcher
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.auto.models import Auto
from bot.core.config import (
    DEBUG,
    ADMIN_TELEGRAM_ID,
    ADMIN_NAME,
    AUTO_1_IDENTIFIER,
    AUTO_1_FUEL_PRICE,
    AUTO_1_CONSUMPTION,
    AUTO_1_MULTIPlIER,
)
from bot.core.db import engine, Base, async_session
from bot.user.models import User, Permissions


async def get_super_user(session: AsyncSession) -> Optional[User]:
    query = select(User).where(User.telegram_id == ADMIN_TELEGRAM_ID)
    result = await session.execute(query)
    return result.first()


async def create_admin(session: AsyncSession) -> None:
    if await get_super_user(session) is None:
        session.add(User(telegram_id=ADMIN_TELEGRAM_ID, name=ADMIN_NAME, role=Permissions.SUPER_ADMIN))


async def create_autos(session: AsyncSession) -> None:
    query = select(Auto).where(Auto.identifier == AUTO_1_IDENTIFIER)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            Auto(
                fuel_price=AUTO_1_FUEL_PRICE,
                consumption=AUTO_1_CONSUMPTION,
                multiplier=AUTO_1_MULTIPlIER,
                identifier=AUTO_1_IDENTIFIER,
            )
        )


async def on_startup(_: Dispatcher):
    async with engine.begin() as conn:
        if DEBUG:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await create_admin(session)
        await create_autos(session)

        await session.commit()
