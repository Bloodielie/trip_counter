from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.balance.services import get_user_balance, get_all_users_balance
from bot.shared import text
import bot.menu.text as menu_text
from bot.menu.keyboards import menu_keyboard, choice_history_type_keyboard
from bot.menu.states import States
from bot.user.models import Permissions, User


async def start(msg: types.Message) -> None:
    await States.menu.set()

    await msg.answer(menu_text.START, reply_markup=menu_keyboard)


async def bad_menu_input(msg: types.Message):
    return await msg.reply(text.BAD_INPUT)


async def menu_user_balance(msg: types.Message, user: User, session: sessionmaker):
    if user.role != Permissions.SUPER_ADMIN:
        async with session() as async_session:
            balance = await get_user_balance(async_session, user.id)

        if balance is None:
            return await msg.answer(menu_text.NO_DATA)
        return await msg.answer(menu_text.USER_BALANCE.format(balance=balance))

    async with session() as async_session:
        balances = await get_all_users_balance(async_session)

    if not balances:
        return await msg.answer(menu_text.NO_DATA)
    return await msg.answer(
        "\n".join([menu_text.USERS_BALANCES.format(balance[0], balance[1]) for balance in balances])
    )


async def menu_history(msg: types.Message, state: FSMContext):
    await state.set_state(States.history.get_history)

    return await msg.answer(menu_text.CHOICE_HISTORY_TYPE, reply_markup=choice_history_type_keyboard)


async def bad_history_input(msg: types.Message):
    await msg.reply(text.BAD_INPUT)
