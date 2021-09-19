import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from bot.config import BOT_TOKEN
from bot.handlers import start, setup_handlers

logging.basicConfig(level=logging.INFO)


def setup_middlewares(dp):
    pass


def create_bot():
    bot = Bot(token=BOT_TOKEN)

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    setup_middlewares(dp)
    setup_handlers(dp)

    return dp


dp = create_bot()
executor.start_polling(dp, skip_updates=True)
