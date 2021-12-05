from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

import bot.menu.text as menu_text
from bot.balance.services import get_user_balance, get_all_users_balance
from bot.menu.keyboards import menu_keyboard, choice_history_type_keyboard
from bot.menu.states import States
from bot.shared import text
from bot.user.models import User
from bot.user.services.invite import get_invite_by_hash
from bot.user.services.user import create_user


async def start(msg: types.Message, session: sessionmaker) -> types.Message:
    _, _, hash_ = msg.text.partition(" ")
    if hash_:
        try:
            async with session.begin() as async_session:
                invite = await get_invite_by_hash(async_session, hash_)
                if invite is None:
                    return await msg.answer(text.PERMISSION_ERROR)
                if invite.invited is not None:
                    return await msg.answer(menu_text.INVITE_ALREADY_ACTIVE)

                await create_user(async_session, msg.from_user.id, invite.user_identifier)
        except IntegrityError:
            return await msg.answer(menu_text.USER_ALREADY_IN_DB)

    await States.menu.set()
    return await msg.answer(menu_text.START, reply_markup=menu_keyboard)


async def bad_menu_input(msg: types.Message):
    return await msg.reply(text.BAD_INPUT)


async def menu_user_balance(msg: types.Message, user: User, session: sessionmaker):
    balance_text = None
    if "admin" not in {role.codename for role in user.roles}:
        async with session() as async_session:
            balance = await get_user_balance(async_session, user.id)

        if balance is not None:
            balance_text = menu_text.USER_BALANCE.format(balance=balance)
    else:
        async with session() as async_session:
            balances = await get_all_users_balance(async_session)

        if balances:
            balance_text = "\n".join([menu_text.USERS_BALANCES.format(balance[0], balance[1]) for balance in balances])

    if balance_text is None:
        return await msg.answer(menu_text.NO_DATA)

    return await msg.answer(balance_text)


async def menu_history(msg: types.Message, state: FSMContext):
    await state.set_state(States.history.get_history)

    return await msg.answer(menu_text.CHOICE_HISTORY_TYPE, reply_markup=choice_history_type_keyboard)


async def bad_history_input(msg: types.Message):
    await msg.reply(text.BAD_INPUT)
