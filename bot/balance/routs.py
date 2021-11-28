from aiogram import Dispatcher

from bot.balance.handlers import start_adding_balance, select_user, input_amount, input_amount_back
from bot.balance.states import AddBalanceStates
from bot.shared import text
from bot.shared.filters import RoleFilter


def setup_commands_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(
        start_adding_balance, RoleFilter(["admin"]), commands="add_balance", state="*"
    )


def setup_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(
        select_user, RoleFilter(["admin"]), state=AddBalanceStates.select_user
    )

    dp.register_message_handler(
        input_amount_back,
        RoleFilter(["admin"]),
        text=[text.BACK],
        state=AddBalanceStates.input_amount,
    )
    dp.register_message_handler(
        input_amount, RoleFilter(["admin"]), state=AddBalanceStates.input_amount
    )
