from aiogram import Dispatcher

from bot.shared import text
from bot.shared.filters import PermissionFilter
from bot.shared.handlers import menu_handler
from bot.user.models import Permissions


def setup_commands_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(menu_handler, PermissionFilter(tuple(iter(Permissions))), commands=["menu"], state="*")


def setup_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(menu_handler, PermissionFilter(tuple(iter(Permissions))), text=[text.MENU], state="*")
