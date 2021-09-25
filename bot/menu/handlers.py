from dataclasses import asdict

from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.balance.services import get_user_balance, get_all_users_balance, get_user_transactions
from bot.shared import text
from bot.menu.keyboards import menu_keyboard, choice_history_type_keyboard
from bot.menu.states import States
from bot.trip.services import get_user_trips
from bot.user.models import Permissions, User


async def start(msg: types.Message) -> None:
    await States.menu.set()

    await msg.answer(text.START, reply_markup=menu_keyboard)


async def bad_menu_input(msg: types.Message):
    return await msg.reply(text.BAD_INPUT)


async def menu_user_balance(msg: types.Message, user: User, session: sessionmaker):
    if user.role != Permissions.SUPER_ADMIN:
        async with session() as async_session:
            balance = await get_user_balance(async_session, user)

        if balance is None:
            return await msg.answer(text.NO_DATA)
        return await msg.answer(text.USER_BALANCE.format(balance=balance))

    async with session() as async_session:
        balances = await get_all_users_balance(async_session)

    if not balances:
        return await msg.answer(text.NO_DATA)
    return await msg.answer("\n".join([text.USERS_BALANCES.format(balance[0], balance[1]) for balance in balances]))


async def menu_history(msg: types.Message, state: FSMContext):
    await state.set_state(States.history.get_history)

    return await msg.answer(text.CHOICE_HISTORY_TYPE, reply_markup=choice_history_type_keyboard)


async def bad_history_input(msg: types.Message):
    await msg.reply(text.BAD_INPUT)


async def get_trips_history(msg: types.Message, user: User, session: sessionmaker):
    async with session() as async_session:
        trips = await get_user_trips(async_session, user)

    if not trips:
        return await msg.answer(text.NO_DATA)

    for trip in trips:
        trip.date = trip.date.strftime("%H:%M:%S %B %d, %Y")

    return await msg.answer("\n".join(text.USER_TRIP.format(**asdict(trip)) for trip in trips))


async def get_transaction_history(msg: types.Message, user: User, session: sessionmaker):
    async with session() as async_session:
        transactions = await get_user_transactions(async_session, user)

    if not transactions:
        return await msg.answer(text.NO_DATA)

    return await msg.answer(
        "\n".join(
            [
                text.USER_TRANSACTION.format(transaction.date.strftime("%H:%M:%S %B %d, %Y"), transaction.amount)
                for transaction in transactions
            ]
        )
    )
