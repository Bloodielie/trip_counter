from decimal import Decimal
from typing import Optional

from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from bot.settings.config import (
    DEBUG,
    ADMIN_TELEGRAM_ID,
    ADMIN_NAME,
    AUTO_1_IDENTIFIER,
    AUTO_1_CONSUMPTION,
    AUTO_1_MULTIPlIER,
    DIESEL_IDENTIFIER,
    DIESEL_PRICE,
    PERMISSION_ADMIN_CODENAME,
    PERMISSION_DRIVER_CODENAME,
    PERMISSION_PASSENGER_CODENAME,
)
from bot.settings.db import engine, Base, async_session
from bot.trip.services.auto import get_auto_by_identifier, create_auto
from bot.trip.services.fuel import get_fuel_by_identifier, create_fuel
from bot.user.models import User
from bot.user.services.role import get_role_by_codename, create_role, add_role_to_user
from bot.user.services.user import get_user_by_tg_id, create_user


async def create_roles(session: AsyncSession) -> None:
    admin_role = await get_role_by_codename(session, PERMISSION_ADMIN_CODENAME)
    if admin_role is None:
        await create_role(session, PERMISSION_ADMIN_CODENAME)

    driver_role = await get_role_by_codename(session, PERMISSION_DRIVER_CODENAME)
    if driver_role is None:
        await create_role(session, PERMISSION_DRIVER_CODENAME)

    passenger_role = await get_role_by_codename(session, PERMISSION_PASSENGER_CODENAME)
    if passenger_role is None:
        await create_role(session, PERMISSION_PASSENGER_CODENAME)

    await session.flush()


async def create_admin(session: AsyncSession) -> User:
    user = await get_user_by_tg_id(session, ADMIN_TELEGRAM_ID)
    if user is None:
        user = await create_user(session, ADMIN_TELEGRAM_ID, ADMIN_NAME)
        await session.flush()

        await add_role_to_user(session, PERMISSION_ADMIN_CODENAME, user.id)
        await add_role_to_user(session, PERMISSION_DRIVER_CODENAME, user.id)
        await add_role_to_user(session, PERMISSION_PASSENGER_CODENAME, user.id)
        await session.flush()

    return user


async def create_fuels(session: AsyncSession) -> None:
    diesel = await get_fuel_by_identifier(session, DIESEL_IDENTIFIER)
    if diesel is None:
        await create_fuel(session, DIESEL_IDENTIFIER, Decimal(DIESEL_PRICE))
        await session.flush()


async def create_autos(session: AsyncSession, owner: User) -> None:
    auto_1 = await get_auto_by_identifier(session, AUTO_1_IDENTIFIER)
    diesel = await get_fuel_by_identifier(session, DIESEL_IDENTIFIER)
    if auto_1 is None and diesel is not None:
        await create_auto(session, AUTO_1_IDENTIFIER, AUTO_1_MULTIPlIER, AUTO_1_CONSUMPTION, owner.id, diesel.id)
        await session.flush()


async def on_startup(_: Dispatcher):
    async with engine.begin() as conn:
        if DEBUG:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async with async_session.begin() as session:
        await create_roles(session)
        owner = await create_admin(session)
        await create_fuels(session)
        await create_autos(session, owner)

        await session.commit()
