from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.auto.keyboards import get_user_keyboard, back_keyboard
from bot.balance.models import Transaction
from bot.balance.states import AddBalanceStates
from bot.core import text
from bot.core.filter import PermissionFilter
from bot.start.keyboards import menu_keyboard
from bot.start.states import States
from bot.user.models import Permissions
from bot.user.services import get_users, get_user_by_name


async def balance_init(msg: types.Message, state: FSMContext, session: sessionmaker):
    async with session() as async_session:
        users = await get_users(async_session)
    keyboard = get_user_keyboard(users)

    async with state.proxy() as data:
        data["users_name"] = [user.name for user in users]

    await state.set_state(AddBalanceStates.select_user)

    return await msg.answer(text.SELECT_USER, reply_markup=keyboard)


async def select_user(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        users_name = data["users_name"]

    if msg.text == text.MENU:
        await state.set_state(States.menu)
        return await msg.answer(text.MENU, reply_markup=menu_keyboard)

    if msg.text not in users_name:
        return await msg.answer(text.BAD_INPUT)

    async with state.proxy() as data:
        data["select_user"] = msg.text

    await state.set_state(AddBalanceStates.input_amount)

    return await msg.answer(text.INPUT_AMOUNT, reply_markup=back_keyboard)


async def input_amount(msg: types.Message, state: FSMContext, session: sessionmaker):
    async with state.proxy() as data:
        selected_user = data["select_user"]

    if msg.text == text.BACK:
        await state.set_state(AddBalanceStates.select_user)
        async with session() as async_session:
            users = await get_users(async_session)
        keyboard = get_user_keyboard(users)
        return await msg.answer(text.SELECT_USER, reply_markup=keyboard)

    try:
        amount = float(msg.text)

        async with session() as async_session:
            user = await get_user_by_name(async_session, selected_user)

            transaction = Transaction(user=user.id, amount=amount)
            async_session.add(transaction)

            await async_session.commit()

        await state.set_state(States.menu)
        return await msg.answer(text.BALANCE_ADDED, reply_markup=menu_keyboard)
    except ValueError:
        await msg.reply(text.BAD_INPUT)


def setup_command_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        balance_init, PermissionFilter([Permissions.SUPER_ADMIN]), commands="add_balance", state="*"
    )


def setup_state_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        select_user, PermissionFilter([Permissions.SUPER_ADMIN]), state=AddBalanceStates.select_user
    )
    dp.register_message_handler(
        input_amount, PermissionFilter([Permissions.SUPER_ADMIN]), state=AddBalanceStates.input_amount
    )
