from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot import text
from bot.keyboards import menu_keyboard


class States(StatesGroup):
    menu = State()
    add_trip = State()
    add_balance = State()
    balance = State()
    history = State()


async def start(msg: types.Message) -> None:
    await States.menu.set()

    await msg.answer(text.START, reply_markup=menu_keyboard)


async def menu(msg: types.Message) -> None:
    print(msg)
    if msg.text == text.ADD_TRIP:
        await States.add_trip.set()
    elif msg.text == text.ADD_BALANCE:
        await States.add_balance.set()
    elif msg.text == text.BALANCE:
        await States.balance.set()
    elif msg.text == text.HISTORY:
        await States.history.set()
    else:
        await msg.reply(text.BAD_INPUT)


def setup_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(menu, state=States.menu)
