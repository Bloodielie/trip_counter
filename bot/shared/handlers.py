from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.menu.keyboards import menu_keyboard
from bot.menu.states import States
from bot.shared import text


async def menu_handler(msg: types.Message, state: FSMContext):
    await state.set_state(States.menu)
    return await msg.answer(text.MENU, reply_markup=menu_keyboard)
