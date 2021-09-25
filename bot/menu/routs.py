from aiogram import Dispatcher

from bot.menu.handlers import (
    start,
    bad_history_input,
    menu_user_balance,
    menu_history,
    bad_menu_input,
    get_trips_history,
    get_transaction_history,
)
from bot.menu.states import States
from bot.shared import text
from bot.shared.filters import PermissionFilter
from bot.user.models import Permissions


def setup_commands_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(start, PermissionFilter(tuple(iter(Permissions))), commands="start", state="*")


def setup_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(
        menu_user_balance, PermissionFilter(tuple(iter(Permissions))), text=[text.BALANCE], state=States.menu
    )
    dp.register_message_handler(
        menu_history, PermissionFilter(tuple(iter(Permissions))), text=[text.HISTORY], state=States.menu
    )
    dp.register_message_handler(bad_menu_input, PermissionFilter(tuple(iter(Permissions))), state=States.menu)

    dp.register_message_handler(
        get_trips_history,
        PermissionFilter(tuple(iter(Permissions))),
        text=[text.TRIP_HISTORY],
        state=States.history.get_history,
    )
    dp.register_message_handler(
        get_transaction_history,
        PermissionFilter(tuple(iter(Permissions))),
        text=[text.TRANSACTION_HISTORY],
        state=States.history.get_history,
    )
    dp.register_message_handler(
        bad_history_input, PermissionFilter(tuple(iter(Permissions))), state=States.history.get_history
    )
