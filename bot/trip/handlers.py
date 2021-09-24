from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.auto.services import get_autos, get_auto_by_identifier
from bot.balance.models import Transaction
from bot.core import text
from bot.core.filter import PermissionFilter
from bot.core.text import INPUT_USERS
from bot.start.keyboards import menu_keyboard
from bot.start.states import States
from bot.trip.keyboards import get_users_keyboard, select_distance_keyboard, confirm_trip_keyboard, get_autos_keyboard
from bot.trip.models import Trip
from bot.trip.services import get_travel_cost
from bot.trip.states import TripStates
from bot.user.models import Permissions, User
from bot.user.services import get_users, get_users_by_names


async def trip_init(msg: types.Message, state: FSMContext):
    await state.set_state(TripStates.input_distance)

    await msg.answer(text.INPUT_DISTANCE, reply_markup=select_distance_keyboard)


async def get_distance(msg: types.Message, state: FSMContext, session: sessionmaker):
    msg_text = msg.text
    if msg_text == text.MENU:
        await state.set_state(States.menu)
        return await msg.answer(text.MENU, reply_markup=menu_keyboard)

    try:
        distance = float(msg_text)
        async with session() as async_session:
            autos = await get_autos(async_session)

        async with state.proxy() as data:
            data['distance'] = distance
            data["autos"] = [auto.identifier for auto in autos]

        await state.set_state(TripStates.select_auto)

        keyboard = get_autos_keyboard(autos)
        await msg.answer(text.INPUT_AUTO, reply_markup=keyboard)
    except ValueError:
        await msg.reply(text.BAD_INPUT)


async def select_auto(msg: types.Message, state: FSMContext, session: sessionmaker):
    msg_text = msg.text
    async with state.proxy() as data:
        autos = data["autos"]

    if msg_text == text.BACK:
        await state.set_state(TripStates.input_distance)
        return await msg.answer(text.INPUT_DISTANCE, reply_markup=select_distance_keyboard)

    if msg_text in autos:
        async with session() as async_session:
            users = await get_users(async_session)

        async with state.proxy() as data:
            data["selected_auto"] = msg_text
            data['users_names'] = [user.name for user in users]
            data['selected_users_names'] = []

        await state.set_state(TripStates.select_users)

        keyboard = get_users_keyboard(users)
        return await msg.answer(INPUT_USERS, reply_markup=keyboard)

    return await msg.reply(text.BAD_INPUT)


async def select_users(msg: types.Message, state: FSMContext):
    msg_text = msg.text
    async with state.proxy() as data:
        users_names = data['users_names']
        selected_users_names = data['selected_users_names']
        distance = data['distance']
        autos = data['autos']
        selected_auto = data['selected_auto']

    if msg_text == text.BACK:
        await state.set_state(TripStates.select_auto)

        keyboard = get_autos_keyboard(autos)
        await msg.answer(text.INPUT_AUTO, reply_markup=keyboard)

    if msg_text == text.COMPLETE and selected_users_names:
        await state.set_state(TripStates.add_trip)

        return await msg.answer(
            text.TRIP_INFO.format(
                distance=distance, auto=selected_auto, select_users=", ".join(selected_users_names)
            ),
            parse_mode="Markdown",
            reply_markup=confirm_trip_keyboard
        )
    if msg_text == text.COMPLETE:
        return await msg.answer(text.NOT_SELECTED_USERS)

    if msg_text not in users_names:
        return await msg.reply(text.BAD_INPUT)

    if msg_text in selected_users_names:
        return await msg.reply(text.USER_ALREADY_SELECT)

    async with state.proxy() as data:
        data['selected_users_names'].append(msg_text)

    return await msg.answer(text.SELECT_NEXT_USER)


async def add_trip(msg: types.Message, state: FSMContext, user: User, session: sessionmaker):
    msg_text = msg.text
    async with state.proxy() as data:
        selected_users_names = data['selected_users_names']
        distance = data['distance']
        selected_auto = data['selected_auto']

    if msg_text == text.CANCEL:
        await state.set_state(States.menu)
        return await msg.answer(text.MENU, reply_markup=menu_keyboard)

    if msg_text == text.CONFIRM:
        await state.set_state(States.menu)

        async with session() as async_session:
            selected_users = await get_users_by_names(async_session, selected_users_names)
            auto = await get_auto_by_identifier(async_session, selected_auto)

            travel_cost = get_travel_cost(auto, distance)
            trip_cost = travel_cost / len(selected_users)

            trip = Trip(creator=user.id, distance=distance, auto=auto.id, cost=trip_cost)
            for selected_user in selected_users:
                trip.users.append(selected_user)
            async_session.add(trip)

            for selected_user in selected_users:
                transaction = Transaction(user=selected_user.id, amount=-trip_cost)
                async_session.add(transaction)

            await async_session.commit()

        return await msg.answer(text.CREATED_TRIP.format(trip_cost), parse_mode="Markdown", reply_markup=menu_keyboard)


def setup_command_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        trip_init, PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]), commands=["add_trip"], state="*"
    )


def setup_state_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        get_distance, PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]), state=TripStates.input_distance
    )
    dp.register_message_handler(
        select_auto, PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]), state=TripStates.select_auto
    )
    dp.register_message_handler(
        select_users, PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]), state=TripStates.select_users
    )
    dp.register_message_handler(
        add_trip, PermissionFilter([Permissions.ADMIN, Permissions.SUPER_ADMIN]), state=TripStates.add_trip
    )
