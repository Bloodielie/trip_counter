from aiogram import types

from bot.shared import text

menu_keyboard = (
    types.ReplyKeyboardMarkup(resize_keyboard=True)
    .row(types.KeyboardButton(text.BALANCE),)
    .row(types.KeyboardButton(text.HISTORY))
)

choice_history_type_keyboard = (
    types.ReplyKeyboardMarkup(resize_keyboard=True)
    .row(types.KeyboardButton(text.TRIP_HISTORY))
    .row(types.KeyboardButton(text.TRANSACTION_HISTORY))
    .row(types.KeyboardButton(text.MENU))
)
