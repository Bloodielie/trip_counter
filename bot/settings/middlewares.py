from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.orm import sessionmaker

from bot.user.services.user import get_user_by_tg_id


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
        if isinstance(args[0], types.Message) or isinstance(args[0], types.CallbackQuery):
            user_id = args[0].from_user.id
            async with self._session() as async_session:
                user = await get_user_by_tg_id(async_session, user_id, True)
            args[-1].update({"user": user})

        return await super().trigger(action, args)
