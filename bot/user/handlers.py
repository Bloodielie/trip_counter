from typing import Optional
from uuid import uuid4

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from bot.menu.keyboards import menu_keyboard
from bot.menu.states import States
from bot.user.models import User, Invite
from bot.user.services.invite import create_invite
from bot.user.states import CreateInvite
from bot.user.text import CHOICE_USER_IDENTIFIER, INVITE_INTEGRITY_ERROR


async def choice_user_identifier_(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(CreateInvite.choice_user_identifier)
    await msg.answer(CHOICE_USER_IDENTIFIER)


async def create_invite_(msg: types.Message, user: User, session: sessionmaker, state: FSMContext) -> None:
    user_identifier = msg.text
    hash = str(uuid4())
    bot_username = (await Bot.get_current().me).username
    link = f"https://t.me/{bot_username}?start={hash}"

    invite: Optional[Invite]
    try:
        async with session.begin() as async_session:
            invite = await create_invite(async_session, user.id, hash, user_identifier)
    except IntegrityError:
        invite = None

    await state.set_state(States.menu)
    if invite is not None:
        await msg.answer(link, reply_markup=menu_keyboard)
    else:
        await msg.answer(INVITE_INTEGRITY_ERROR, reply_markup=menu_keyboard)
