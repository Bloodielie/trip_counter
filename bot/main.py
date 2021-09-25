import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from bot.core.config import BOT_TOKEN
from bot.core.db import async_session
from bot.core.events import on_startup
from bot.core.middlewares import InjectMiddleware, AddUserMiddleware
from bot.core.routs import setup_routes

logging.basicConfig(level=logging.INFO)


def setup_middlewares(dp: Dispatcher) -> None:
    dp.setup_middleware(InjectMiddleware({"session": async_session}))
    dp.setup_middleware(AddUserMiddleware(async_session))


def create_dp() -> Dispatcher:
    bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    setup_middlewares(dp)
    setup_routes(dp)

    return dp


executor.start_polling(create_dp(), on_startup=on_startup, skip_updates=True)
