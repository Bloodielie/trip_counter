from aiogram.dispatcher.filters.state import StatesGroup, State


class TripStates(StatesGroup):
    input_distance = State()
    select_auto = State()
    select_users = State()
    add_trip = State()
