from aiogram import Dispatcher

from bot.config import DEBUG
from bot.db import engine, Base


async def on_startup(_: Dispatcher):
    async with engine.begin() as conn:
        if DEBUG:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
