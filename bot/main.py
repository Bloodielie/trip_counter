import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from bot.core.config import BOT_TOKEN
from bot.core.db import async_session
from bot.core.events import on_startup
from bot.core.middlewares import InjectMiddleware, AddUserMiddleware
from bot.start.handlers import setup_state_handlers as start_state_handlers, setup_command_handlers as start_command_handlers
from bot.trip.handlers import setup_state_handlers as trip_state_handlers, setup_command_handlers as trip_command_handlers
from bot.balance.handlers import setup_command_handlers as balance_command_handlers, setup_state_handlers as balance_state_handlers

logging.basicConfig(level=logging.INFO)


def setup_middlewares(dp: Dispatcher) -> None:
    dp.setup_middleware(InjectMiddleware({"session": async_session}))
    dp.setup_middleware(AddUserMiddleware(async_session))


def setup_handlers(dp: Dispatcher) -> None:
    start_command_handlers(dp)
    trip_command_handlers(dp)
    balance_command_handlers(dp)

    start_state_handlers(dp)
    trip_state_handlers(dp)
    balance_state_handlers(dp)


def create_dp() -> Dispatcher:
    bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    setup_middlewares(dp)
    setup_handlers(dp)

    return dp


executor.start_polling(create_dp(), on_startup=on_startup, skip_updates=True)
