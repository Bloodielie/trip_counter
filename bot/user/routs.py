from aiogram import Dispatcher

from bot.shared.filters import RoleFilter
from bot.user.handlers import create_invite_, choice_user_identifier_
from bot.user.states import CreateInvite


def setup_commands_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(choice_user_identifier_, RoleFilter(["admin"]), commands="create_invite", state="*")


def setup_routs(dp: Dispatcher) -> None:
    dp.register_message_handler(create_invite_, RoleFilter(["admin"]), state=CreateInvite.choice_user_identifier)
