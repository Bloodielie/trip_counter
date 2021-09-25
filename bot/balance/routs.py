from aiogram import Dispatcher

from bot.balance.handlers import start_adding_balance, select_user, input_amount, input_amount_back
from bot.balance.states import AddBalanceStates
from bot.shared import text
from bot.shared.filters import PermissionFilter
from bot.user.models import Permissions


def setup_commands_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(
        start_adding_balance, PermissionFilter([Permissions.SUPER_ADMIN]), commands="add_balance", state="*"
    )


def setup_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(
        select_user, PermissionFilter([Permissions.SUPER_ADMIN]), state=AddBalanceStates.select_user
    )

    dp.register_message_handler(
        input_amount_back,
        PermissionFilter([Permissions.SUPER_ADMIN]),
        text=[text.BACK],
        state=AddBalanceStates.input_amount,
    )
    dp.register_message_handler(
        input_amount, PermissionFilter([Permissions.SUPER_ADMIN]), state=AddBalanceStates.input_amount
    )
