from aiogram.dispatcher.filters.state import StatesGroup, State


class HistoryStates(StatesGroup):
    get_history = State()


class States(StatesGroup):
    menu = State()
    history = HistoryStates
