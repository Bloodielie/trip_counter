from aiogram import Dispatcher

from bot.shared import text
from bot.shared.filters import RoleFilter
from bot.shared.handlers import menu_handler


def setup_commands_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(menu_handler, RoleFilter("*"), commands=["menu"], state="*")


def setup_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(menu_handler, RoleFilter("*"), text=[text.MENU], state="*")
