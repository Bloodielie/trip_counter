from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.auto.services import get_autos, get_auto_by_identifier
from bot.balance.models import Transaction
from bot.shared import text
from bot.shared.text import INPUT_USERS
from bot.menu.keyboards import menu_keyboard
from bot.menu.states import States
from bot.trip.keyboards import get_users_keyboard, select_distance_keyboard, confirm_trip_keyboard, get_autos_keyboard
from bot.trip.models import Trip
from bot.trip.services import get_travel_cost
from bot.trip.states import TripStates
from bot.user.models import User
from bot.user.services import get_users, get_users_by_names


async def start_creating_trip(msg: types.Message, state: FSMContext):
    await state.set_state(TripStates.input_distance)

    await msg.answer(text.INPUT_DISTANCE, reply_markup=select_distance_keyboard)


async def get_distance(msg: types.Message, state: FSMContext, session: sessionmaker):
    try:
        distance = float(msg.text)
    except ValueError:
        return await msg.reply(text.BAD_INPUT)

    async with session() as async_session:
        autos = await get_autos(async_session)
    auto_identifiers = [auto.identifier for auto in autos]

    async with state.proxy() as data:
        data["distance"] = distance
        data["autos"] = auto_identifiers

    await state.set_state(TripStates.select_auto)

    keyboard = get_autos_keyboard(auto_identifiers)
    return await msg.answer(text.INPUT_AUTO, reply_markup=keyboard)


async def select_auto_back(msg: types.Message, state: FSMContext):
    await state.set_state(TripStates.input_distance)

    return await msg.answer(text.INPUT_DISTANCE, reply_markup=select_distance_keyboard)


async def select_auto(msg: types.Message, state: FSMContext, session: sessionmaker, user: User):
    async with state.proxy() as data:
        autos = data["autos"]

    if msg.text not in autos:
        return await msg.reply(text.BAD_INPUT)

    async with session() as async_session:
        users = await get_users(async_session)

    async with state.proxy() as data:
        data["selected_auto"] = msg.text
        data["users_names"] = [user.name for user in users]
        data["selected_users_names"] = [user.name]

    await state.set_state(TripStates.select_users)

    keyboard = get_users_keyboard(users, user)
    return await msg.answer(INPUT_USERS, reply_markup=keyboard)


async def select_users_back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        autos = data["autos"]

    await state.set_state(TripStates.select_auto)

    keyboard = get_autos_keyboard(autos)
    await msg.answer(text.INPUT_AUTO, reply_markup=keyboard)


async def select_users(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_names = data["users_names"]
        selected_users_names = data["selected_users_names"]

    if msg.text not in user_names:
        return await msg.reply(text.BAD_INPUT)

    if msg.text in selected_users_names:
        return await msg.reply(text.USER_ALREADY_SELECT)

    async with state.proxy() as data:
        data["selected_users_names"].append(msg.text)

    return await msg.answer(text.SELECT_NEXT_USER)


async def complete_select_users(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        selected_users_names = data["selected_users_names"]
        distance = data["distance"]
        selected_auto = data["selected_auto"]

    if selected_users_names:
        await state.set_state(TripStates.add_trip)

        return await msg.answer(
            text.TRIP_INFO.format(distance=distance, auto=selected_auto, select_users=", ".join(selected_users_names)),
            parse_mode="Markdown",
            reply_markup=confirm_trip_keyboard,
        )

    return await msg.answer(text.NOT_SELECTED_USERS)


async def cancel_add_trip(msg: types.Message, state: FSMContext):
    await state.set_state(States.menu)

    return await msg.answer(text.MENU, reply_markup=menu_keyboard)


async def confirm_add_trip(msg: types.Message, state: FSMContext, user: User, session: sessionmaker):
    async with state.proxy() as data:
        selected_users_names = data["selected_users_names"]
        distance = data["distance"]
        selected_auto = data["selected_auto"]

    async with session() as async_session:
        selected_users = await get_users_by_names(async_session, selected_users_names)
        auto = await get_auto_by_identifier(async_session, selected_auto)

        travel_cost = get_travel_cost(auto.consumption, auto.fuel_price, auto.multiplier, distance)
        trip_cost = travel_cost / len(selected_users_names)

        trip = Trip(creator=user.id, distance=distance, auto=auto.id, cost=trip_cost)
        for selected_user in selected_users:
            trip.users.append(selected_user)
        async_session.add(trip)

        for selected_user in selected_users:
            transaction = Transaction(user=selected_user.id, amount=-trip_cost)
            async_session.add(transaction)

        await async_session.commit()

    await state.set_state(States.menu)

    return await msg.answer(text.CREATED_TRIP.format(trip_cost), parse_mode="Markdown", reply_markup=menu_keyboard)
