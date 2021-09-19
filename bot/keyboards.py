from aiogram import types

from bot import text

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(
    types.KeyboardButton(text.ADD_TRIP),
    types.KeyboardButton(text.ADD_BALANCE),
).row(
    types.KeyboardButton(text.BALANCE),
    types.KeyboardButton(text.HISTORY),
)
