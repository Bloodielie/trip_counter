from aiogram.dispatcher.filters.state import StatesGroup, State


class HistoryStates(StatesGroup):
    choice_history_type = State()
    trip_history = State()
    transaction_history = State()


class States(StatesGroup):
    menu = State()
    history = HistoryStates
