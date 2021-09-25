from typing import Sequence

from aiogram import types
from aiogram.dispatcher.filters import Filter
from aiogram.dispatcher.handler import ctx_data

from bot.shared import text
from bot.user.models import Permissions


class PermissionFilter(Filter):
    def __init__(self, permissions: Sequence[Permissions]):
        self._permissions = permissions

    async def check(self, msg: types.Message) -> bool:
        data = ctx_data.get()
        try:
            user = data["user"]
        except KeyError:
            await msg.answer(text.PERMISSION_ERROR)
            return False

        if user is None:
            await msg.answer(text.PERMISSION_ERROR)
            return False

        if user.role in self._permissions:
            return True

        await msg.answer(text.PERMISSION_ERROR)
        return False
