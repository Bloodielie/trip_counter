import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot.settings.config import BOT_TOKEN, PATH_TO_STATES, DEBUG, LIMIT_EVENTS_PER_MIN
from bot.settings.db import async_session
from bot.settings.middlewares import InjectMiddleware, AddUserMiddleware, ThrottlingMiddleware
from bot.settings.routs import setup_routes

logging.basicConfig(level=logging.INFO if not DEBUG else logging.DEBUG)


def setup_middlewares(dp: Dispatcher, bot: Bot) -> None:
    loop = asyncio.get_event_loop()
    dp.setup_middleware(ThrottlingMiddleware(LIMIT_EVENTS_PER_MIN, bot, loop))

    dp.setup_middleware(InjectMiddleware({"session": async_session}))
    dp.setup_middleware(AddUserMiddleware(async_session))
    dp.setup_middleware(LoggingMiddleware("bot"))


def create_dp() -> Dispatcher:
    bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")

    storage = JSONStorage(PATH_TO_STATES)
    dp = Dispatcher(bot, storage=storage)

    setup_middlewares(dp, bot)
    setup_routes(dp)

    return dp
