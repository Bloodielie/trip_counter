import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.utils import executor

from bot.settings.config import BOT_TOKEN, PATH_TO_STATES, DEBUG
from bot.settings.db import async_session
from bot.settings.events import on_startup
from bot.settings.middlewares import InjectMiddleware, AddUserMiddleware
from bot.settings.routs import setup_routes

logging.basicConfig(level=logging.INFO if not DEBUG else logging.DEBUG)


def setup_middlewares(dp: Dispatcher) -> None:
    dp.setup_middleware(InjectMiddleware({"session": async_session}))
    dp.setup_middleware(AddUserMiddleware(async_session))


def create_dp() -> Dispatcher:
    bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")

    storage = JSONStorage(PATH_TO_STATES)
    dp = Dispatcher(bot, storage=storage)

    setup_middlewares(dp)
    setup_routes(dp)

    return dp


executor.start_polling(create_dp(), on_startup=on_startup, skip_updates=True)
