from aiogram import Dispatcher

from bot.shared import text
from bot.shared.filters import PermissionFilter
from bot.trip.handlers import (
    start_creating_trip,
    get_distance,
    select_auto,
    select_users,
    select_users_back,
    complete_select_users,
    cancel_add_trip,
    confirm_add_trip,
)
from bot.trip.states import TripStates
from bot.user.models import Permissions


def setup_commands_routs(dp: Dispatcher) -> None:
    # create_trip
    dp.register_message_handler(
        start_creating_trip,
        PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]),
        commands=["add_trip"],
        state="*",
    )


def setup_routs(dp: Dispatcher) -> None:
    # create_trip
    dp.register_message_handler(
        get_distance, PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]), state=TripStates.input_distance
    )

    dp.register_message_handler(
        start_creating_trip,
        PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]),
        text=[text.BACK],
        state=TripStates.select_auto,
    )
    dp.register_message_handler(
        select_auto, PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]), state=TripStates.select_auto
    )

    dp.register_message_handler(
        select_users_back,
        PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]),
        text=[text.BACK],
        state=TripStates.select_users,
    )
    dp.register_message_handler(
        complete_select_users,
        PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]),
        text=[text.COMPLETE],
        state=TripStates.select_users,
    )
    dp.register_message_handler(
        select_users, PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]), state=TripStates.select_users
    )

    dp.register_message_handler(
        cancel_add_trip,
        PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]),
        text=[text.CANCEL],
        state=TripStates.add_trip,
    )
    dp.register_message_handler(
        confirm_add_trip,
        PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]),
        text=[text.CONFIRM],
        state=TripStates.add_trip,
    )
