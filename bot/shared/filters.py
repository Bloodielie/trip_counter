from typing import Sequence, Set

from aiogram import types
from aiogram.dispatcher.filters import Filter
from aiogram.dispatcher.handler import ctx_data

from bot.shared import text
from bot.user.models import Role


def check_roles(roles: Sequence[Role], codenames: Set[str]) -> bool:
    for role in roles:
        if role.codename in codenames:
            return True

    return False


class RoleFilter(Filter):
    def __init__(self, roles: Sequence[str]):
        self._roles = set(roles)

    async def check(self, msg: types.Message) -> bool:
        data = ctx_data.get()
        user = data.get("user")
        if user is None:
            await msg.answer(text.PERMISSION_ERROR)
            return False

        if "*" in self._roles:
            return True

        if not check_roles(user.roles, self._roles):
            await msg.answer(text.PERMISSION_ERROR)
            return False

        return True
