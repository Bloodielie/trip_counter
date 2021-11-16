from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.balance.models import Transaction
from bot.shared import text
from bot.menu.keyboards import menu_keyboard
from bot.menu.states import States
from bot.trip.keyboards import select_distance_keyboard, confirm_trip_keyboard, get_autos_keyboard, get_choice_users_keyboard
from bot.trip.models import Trip
from bot.trip.services.trip import get_travel_cost
from bot.trip.services.auto import get_user_autos, get_auto_params_by_identifier
from bot.trip.states import TripStates
import bot.trip.text as trip_text
from bot.user.models import User
from bot.user.services import get_users, get_users_by_identifiers, update_user_balance


async def start_creating_trip(msg: types.Message, state: FSMContext):
    await state.set_state(TripStates.input_distance)
    await msg.answer(trip_text.INPUT_DISTANCE, reply_markup=select_distance_keyboard)


async def get_distance(msg: types.Message, state: FSMContext, session: sessionmaker, user: User):
    try:
        distance = float(msg.text)
    except ValueError:
        return await msg.reply(text.BAD_INPUT)

    async with session() as async_session:
        user_autos = await get_user_autos(async_session, user.id)
    if not user_autos:
        await state.set_state(States.menu)
        return await msg.reply(trip_text.USER_HAS_NO_AUTOS, reply_markup=menu_keyboard)

    autos_identifiers = [auto.identifier for auto in user_autos]

    async with state.proxy() as data:
        data["distance"] = distance
        data["autos"] = autos_identifiers

    await state.set_state(TripStates.select_auto)

    keyboard = get_autos_keyboard(autos_identifiers)
    return await msg.answer(trip_text.INPUT_AUTO, reply_markup=keyboard)


async def select_auto(msg: types.Message, state: FSMContext, session: sessionmaker, user: User):
    driver = user
    async with state.proxy() as data:
        autos = data["autos"]

    if msg.text not in autos:
        return await msg.reply(text.BAD_INPUT)

    async with session() as async_session:
        users = await get_users(async_session)

    passengers_identifiers = [user.identifier for user in users if user.id != driver.id]

    async with state.proxy() as data:
        data["selected_auto"] = msg.text
        data["passengers_identifiers"] = passengers_identifiers
        data["selected_passengers"] = []

    await state.set_state(TripStates.select_users)

    keyboard = get_choice_users_keyboard(passengers_identifiers)
    return await msg.answer(trip_text.INPUT_USERS, reply_markup=keyboard)


async def select_users_back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        autos = data["autos"]

    await state.set_state(TripStates.select_auto)

    keyboard = get_autos_keyboard(autos)
    await msg.answer(trip_text.INPUT_AUTO, reply_markup=keyboard)


async def select_users(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        passengers_identifiers = data["passengers_identifiers"]
        selected_passengers = data["selected_passengers"]

    if msg.text not in passengers_identifiers:
        return await msg.reply(text.BAD_INPUT)

    if msg.text in selected_passengers:
        return await msg.reply(trip_text.USER_ALREADY_SELECT)

    selected_passengers.append(msg.text)
    async with state.proxy() as data:
        data["selected_passengers"] = selected_passengers

    return await msg.answer(trip_text.SELECT_NEXT_USER)


async def complete_select_users(msg: types.Message, state: FSMContext, user: User):
    async with state.proxy() as data:
        selected_passengers = data["selected_passengers"]
        distance = data["distance"]
        selected_auto = data["selected_auto"]

    if selected_passengers:
        await state.set_state(TripStates.add_trip)
        return await msg.answer(
            trip_text.TRIP_INFO.format(
                distance=distance,
                auto=selected_auto,
                driver=user.identifier,
                select_users=", ".join(selected_passengers)
            ),
            parse_mode="Markdown",
            reply_markup=confirm_trip_keyboard,
        )

    return await msg.answer(trip_text.NOT_SELECTED_USERS)


async def cancel_add_trip(msg: types.Message, state: FSMContext):
    await state.set_state(States.menu)

    return await msg.answer(text.MENU, reply_markup=menu_keyboard)


async def confirm_add_trip(msg: types.Message, state: FSMContext, user: User, session: sessionmaker):
    async with state.proxy() as data:
        selected_passengers = data["selected_passengers"]
        distance = data["distance"]
        selected_auto = data["selected_auto"]

    async with session.begin() as async_session:
        selected_users = await get_users_by_identifiers(async_session, selected_passengers)
        auto_params = await get_auto_params_by_identifier(async_session, selected_auto)

        travel_cost = get_travel_cost(auto_params.consumption, auto_params.price, auto_params.multiplier, distance)
        trip_cost = travel_cost / (len(selected_passengers) + 1)

        trip = Trip(driver=user.id, distance=distance, auto=auto_params.id, cost=trip_cost)
        for selected_user in selected_users:
            trip.passengers.append(selected_user)
        async_session.add(trip)

        for selected_user in selected_users:
            transaction = Transaction(amount=trip_cost, sender=selected_user.id, receiver=user.id)
            await update_user_balance(async_session, selected_user.id, -trip_cost)
            await update_user_balance(async_session, user.id, trip_cost)
            async_session.add(transaction)

        await async_session.commit()

    await state.set_state(States.menu)

    return await msg.answer(trip_text.CREATED_TRIP.format(trip_cost), parse_mode="Markdown", reply_markup=menu_keyboard)
