from decimal import Decimal, InvalidOperation

from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.trip.keyboards import back_keyboard, get_users_menu_keyboard
from bot.balance.models import Transaction
from bot.balance.states import AddBalanceStates
from bot.shared import text
import bot.balance.text as balance_text
from bot.menu.keyboards import menu_keyboard
from bot.menu.states import States
from bot.user.services import get_users, get_user_by_identifier, update_user_balance


async def start_adding_balance(msg: types.Message, state: FSMContext, session: sessionmaker):
    async with session() as async_session:
        users = await get_users(async_session)
    usernames = [user.identifier for user in users]

    async with state.proxy() as data:
        data["users_name"] = usernames

    await state.set_state(AddBalanceStates.select_user)

    keyboard = get_users_menu_keyboard(usernames)
    return await msg.answer(balance_text.SELECT_USER, reply_markup=keyboard)


async def select_user(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text not in data["users_name"]:
            return await msg.answer(text.BAD_INPUT)

        data["select_user"] = msg.text

    await state.set_state(AddBalanceStates.input_amount)

    return await msg.answer(balance_text.INPUT_AMOUNT, reply_markup=back_keyboard)


async def input_amount_back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        usernames = data["users_name"]

    await state.set_state(AddBalanceStates.select_user)

    keyboard = get_users_menu_keyboard(usernames)
    return await msg.answer(balance_text.SELECT_USER, reply_markup=keyboard)


async def input_amount(msg: types.Message, state: FSMContext, session: sessionmaker):
    async with state.proxy() as data:
        selected_user = data["select_user"]

    try:
        amount = Decimal(msg.text)
    except InvalidOperation:
        return await msg.reply(text.BAD_INPUT)

    async with session.begin() as async_session:
        user = await get_user_by_identifier(async_session, selected_user)

        transaction = Transaction(amount=amount, receiver=user.id)
        async_session.add(transaction)
        await update_user_balance(async_session, user.id, amount)

        await async_session.commit()

    await state.set_state(States.menu)

    return await msg.answer(balance_text.BALANCE_ADDED, reply_markup=menu_keyboard)
