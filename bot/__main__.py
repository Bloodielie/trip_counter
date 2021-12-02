from aiogram.utils import executor

from bot.main import create_dp
from bot.settings.events import on_startup

if __name__ == "__main__":
    executor.start_polling(create_dp(), on_startup=on_startup, skip_updates=True)
