import asyncio
from asyncio import AbstractEventLoop
from collections import defaultdict
from typing import Optional

from aiogram import types, Bot
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.orm import sessionmaker

from bot.shared.text import EXCEEDED_LIMIT
from bot.user.services.user import get_user_by_tg_id


def _get_user_id(event: TelegramObject) -> Optional[int]:
    user_id = None
    if isinstance(event, types.Message) or isinstance(event, types.CallbackQuery):
        user_id = event.from_user.id

    return user_id


class InjectMiddleware(BaseMiddleware):
    def __init__(self, injects: dict):
        super().__init__()

        self._injects = injects

    async def trigger(self, action, args):
        args[-1].update(self._injects)


class AddUserMiddleware(BaseMiddleware):
    def __init__(self, session: sessionmaker):
        super().__init__()

        self._session = session

    async def trigger(self, action, args):
        user_id = _get_user_id(args[0])
        if user_id is None:
            return None

        async with self._session() as async_session:
            user = await get_user_by_tg_id(async_session, user_id, True)
        args[-1].update({"user": user})


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(
        self, limit_events_per_minute: int, bot: Optional[Bot] = None, loop: Optional[AbstractEventLoop] = None
    ):
        super().__init__()

        self._limit_per_minute = limit_events_per_minute * 3
        self._bot = bot or Bot.get_current()
        self._loop = loop or asyncio.get_running_loop()

        self._users_statistics = defaultdict(int)

        self._loop.call_soon(self.__clear_statistic)

    def __clear_statistic(self) -> None:
        self._users_statistics.clear()
        self._loop.call_later(60, self.__clear_statistic)

    async def trigger(self, action, args) -> None:
        if action.find("update") != -1:
            return None

        event = args[0]
        user_id = _get_user_id(event)
        if user_id is None:
            return None

        self._users_statistics[user_id] += 1
        user_events_count = self._users_statistics[user_id]
        if user_events_count > self._limit_per_minute:
            await self._bot.send_message(user_id, EXCEEDED_LIMIT)
            raise CancelHandler
