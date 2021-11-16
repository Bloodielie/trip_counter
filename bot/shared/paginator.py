import json
from dataclasses import asdict, dataclass
from json import JSONDecodeError
from typing import Callable, Awaitable, TypeVar, List, Optional

from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.user.models import User

T = TypeVar("T")

GetDataFuncType = Callable[[AsyncSession, User, int, int], Awaitable[T]]
FormattingFuncType = Callable[[User, List[T]], str]


@dataclass(frozen=True)
class CallBackData:
    id: str
    offset: int


def get_pagination_keyboard(
    previous_callback_data: CallBackData, next_callback_data: CallBackData
):
    return (
        types.InlineKeyboardMarkup()
        .row(
            types.InlineKeyboardButton("<<", callback_data=json.dumps(asdict(previous_callback_data))),
            types.InlineKeyboardButton(">>", callback_data=json.dumps(asdict(next_callback_data)))
        )
    )


class Paginator:
    def __init__(
        self,
        id_: str,
        get_data_func: GetDataFuncType,
        formatting_func: FormattingFuncType,
        no_data_text: str,
        cursor_at_begin_text: str,
        cursor_at_end_text: str,
        content_amount_on_page: int = 3
    ):
        self._id = id_
        self.next_id = f"{id_}_next"
        self.prev_id = f"{id_}_prev"

        self._get_data_func = get_data_func
        self._formatting_func = formatting_func

        self._no_data_text = no_data_text
        self._cursor_at_begin_text = cursor_at_begin_text
        self._cursor_at_end_text = cursor_at_end_text

        self._content_amount_on_page = content_amount_on_page

    @staticmethod
    def _get_callback_data(callback_query: types.CallbackQuery) -> Optional[CallBackData]:
        try:
            dict_data = json.loads(callback_query.data)
        except JSONDecodeError:
            return None

        try:
            return CallBackData(**dict_data)
        except TypeError:
            return None

    def _check_id_in_callback_data(self, callback_query: types.CallbackQuery, id_: str) -> bool:
        callback_data = self._get_callback_data(callback_query)
        if callback_data is None:
            return False

        return callback_data.id == id_

    def is_next_id(self, callback_query: types.CallbackQuery) -> bool:
        return self._check_id_in_callback_data(callback_query, self.next_id)

    def is_prev_id(self, callback_query: types.CallbackQuery) -> bool:
        return self._check_id_in_callback_data(callback_query, self.prev_id)

    async def message_handler(self, msg: types.Message, user: User, session: sessionmaker):
        async with session() as async_session:
            elements = await self._get_data_func(async_session, user, self._content_amount_on_page, 0)

        if not elements:
            return await msg.answer(self._no_data_text)

        return await msg.answer(
            self._formatting_func(user, elements),
            reply_markup=get_pagination_keyboard(
                CallBackData(id=self.next_id, offset=0), CallBackData(id=self.prev_id, offset=0)
            )
        )

    async def next_callback_query_handler(self, callback_query: types.CallbackQuery, user: User, session: sessionmaker):
        data = self._get_callback_data(callback_query)
        if data is None:
            return await callback_query.answer(self._no_data_text)

        offset = data.offset + self._content_amount_on_page

        async with session() as async_session:
            elements = await self._get_data_func(async_session, user, self._content_amount_on_page, offset)

        if not elements:
            return await callback_query.answer(self._cursor_at_begin_text)

        await callback_query.message.edit_text(self._formatting_func(user, elements))
        await callback_query.message.edit_reply_markup(
            get_pagination_keyboard(
                CallBackData(id=self.next_id, offset=offset), CallBackData(id=self.prev_id, offset=offset)
            )
        )

    async def prev_callback_query_handler(self, callback_query: types.CallbackQuery, user: User, session: sessionmaker):
        data = self._get_callback_data(callback_query)
        if data is None:
            return await callback_query.answer(self._no_data_text)

        if data.offset == 0:
            return await callback_query.answer(self._cursor_at_end_text)

        offset = data.offset - self._content_amount_on_page

        async with session() as async_session:
            elements = await self._get_data_func(async_session, user, self._content_amount_on_page, offset)

        await callback_query.message.edit_text(self._formatting_func(user, elements))
        await callback_query.message.edit_reply_markup(
            get_pagination_keyboard(
                CallBackData(id=self.next_id, offset=offset), CallBackData(id=self.prev_id, offset=offset)
            )
        )
