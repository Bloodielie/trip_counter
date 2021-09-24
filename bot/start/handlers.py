from dataclasses import asdict

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.balance.services import get_user_balance, get_all_users_balance, get_user_transactions
from bot.core import text
from bot.core.filter import PermissionFilter
from bot.core.text import USER_TRANSACTION
from bot.start.keyboards import menu_keyboard, choice_history_type_keyboard
from bot.start.states import States
from bot.trip.services import get_user_trips
from bot.user.models import Permissions, User


async def start(msg: types.Message) -> None:
    await States.menu.set()

    await msg.answer(text.START, reply_markup=menu_keyboard)


async def menu(msg: types.Message, user: User, session: sessionmaker, state: FSMContext):
    if msg.text == text.BALANCE:
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
        return await msg.answer(
            "\n".join([text.USERS_BALANCES.format(balance[0], balance[1]) for balance in balances])
        )
    elif msg.text == text.HISTORY:
        await state.set_state(States.history.choice_history_type)

        return await msg.answer(text.CHOICE_HISTORY_TYPE, reply_markup=choice_history_type_keyboard)
    else:
        await msg.reply(text.BAD_INPUT)


async def choice_history_type(msg: types.Message, user: User, session: sessionmaker):
    if msg.text == text.TRIP_HISTORY:
        async with session() as async_session:
            trips = await get_user_trips(async_session, user)

        if not trips:
            return await msg.answer(text.NO_DATA)

        for trip in trips:
            trip.date = trip.date.strftime("%H:%M:%S  %B  %d, %Y")

        return await msg.answer(
            "\n".join(text.USER_TRIP.format(**asdict(trip)) for trip in trips))
    elif msg.text == text.TRANSACTION_HISTORY:
        async with session() as async_session:
            transactions = await get_user_transactions(async_session, user)

        if not transactions:
            return await msg.answer(text.NO_DATA)

        return await msg.answer(
            "\n".join(
                [text.USER_TRANSACTION.format(transaction.date.strftime("%H:%M:%S  %B  %d, %Y"), transaction.amount) for transaction in transactions]
            )
        )
    else:
        await msg.reply(text.BAD_INPUT)


def setup_command_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start, PermissionFilter(tuple(iter(Permissions))), commands="start", state="*")


def setup_state_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(menu, PermissionFilter(tuple(iter(Permissions))), state=States.menu)
    dp.register_message_handler(
        choice_history_type, PermissionFilter(tuple(iter(Permissions))), state=States.history.choice_history_type
    )
