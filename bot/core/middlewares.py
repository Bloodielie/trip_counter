from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.orm import sessionmaker

from bot.user.services import get_user_by_tg_id


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

    async def on_pre_process_message(self, msg: types.Message, data: dict):
        async with self._session() as async_session:
            user = await get_user_by_tg_id(async_session, msg.from_user.id)

        data["user"] = user
