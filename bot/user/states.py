from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateInvite(StatesGroup):
    choice_user_identifier = State()
