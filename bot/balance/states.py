from aiogram.dispatcher.filters.state import StatesGroup, State


class AddBalanceStates(StatesGroup):
    select_user = State()
    input_amount = State()
