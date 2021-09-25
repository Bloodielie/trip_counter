from aiogram import Dispatcher

from bot.shared.routs import setup_routs as setup_shared_routs, setup_commands_routs as setup_shared_commands_routs
from bot.menu.routs import setup_routs as start_state_handlers, setup_commands_routs as start_command_handlers
from bot.trip.routs import setup_commands_routs as setup_trip_commands_routs, setup_routs as setup_trip_routs
from bot.balance.routs import setup_commands_routs as setup_balance_commands_routs, setup_routs as setup_balance_routs


def setup_routes(dp: Dispatcher) -> None:
    setup_shared_commands_routs(dp)
    start_command_handlers(dp)
    setup_trip_commands_routs(dp)
    setup_balance_commands_routs(dp)

    setup_shared_routs(dp)
    start_state_handlers(dp)
    setup_trip_routs(dp)
    setup_balance_routs(dp)
