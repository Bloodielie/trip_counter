from aiogram import Dispatcher

from bot.balance.services import get_user_transactions
from bot.menu.handlers import (
    start,
    bad_history_input,
    menu_user_balance,
    menu_history,
    bad_menu_input
)
from bot.menu.services import formatting_trips, formatting_transactions
from bot.menu.states import States
from bot.shared import text
from bot.shared.filters import RoleFilter
from bot.shared.paginator import Paginator
from bot.trip.services.trip import get_user_trips_info
import bot.menu.text as menu_text


def setup_commands_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(start, RoleFilter("*"), commands="start", state="*")


def setup_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(
        menu_user_balance, RoleFilter("*"), text=[text.BALANCE], state=States.menu
    )
    dp.register_message_handler(
        menu_history, RoleFilter("*"), text=[text.HISTORY], state=States.menu
    )
    dp.register_message_handler(bad_menu_input, RoleFilter("*"), state=States.menu)

    trip_history_paginator = Paginator(
        "trip_hist",
        menu_text.NO_DATA,
        menu_text.CALLBACK_QUERY_AT_BEGIN,
        menu_text.CALLBACK_QUERY_AT_END,
        3,
        get_user_trips_info,
        formatting_trips
    )
    dp.register_callback_query_handler(
        trip_history_paginator.prev_callback_query_handler,
        trip_history_paginator.is_prev_id,
        state="*"
    )
    dp.register_callback_query_handler(
        trip_history_paginator.next_callback_query_handler,
        trip_history_paginator.is_next_id,
        state="*"
    )
    dp.register_message_handler(
        trip_history_paginator.message_handler,
        RoleFilter("*"),
        text=[text.TRIP_HISTORY],
        state=States.history.get_history,
    )

    transaction_history_paginator = Paginator(
        "transaction_hist",
        menu_text.NO_DATA,
        menu_text.CALLBACK_QUERY_AT_BEGIN,
        menu_text.CALLBACK_QUERY_AT_END,
        6,
        get_user_transactions,
        formatting_transactions
    )
    dp.register_callback_query_handler(
        transaction_history_paginator.prev_callback_query_handler,
        transaction_history_paginator.is_prev_id,
        state="*"
    )
    dp.register_callback_query_handler(
        transaction_history_paginator.next_callback_query_handler,
        transaction_history_paginator.is_next_id,
        state="*"
    )
    dp.register_message_handler(
        transaction_history_paginator.message_handler,
        RoleFilter("*"),
        text=[text.TRANSACTION_HISTORY],
        state=States.history.get_history,
    )

    dp.register_message_handler(
        bad_history_input, RoleFilter("*"), state=States.history.get_history
    )
