from aiogram import types

from bot.shared import text

menu_keyboard = (
    types.ReplyKeyboardMarkup(resize_keyboard=True)
    .row(
        types.KeyboardButton(text.BALANCE),
    )
    .row(types.KeyboardButton(text.HISTORY))
)

choice_history_type_keyboard = (
    types.ReplyKeyboardMarkup(resize_keyboard=True)
    .row(types.KeyboardButton(text.TRIP_HISTORY))
    .row(types.KeyboardButton(text.TRANSACTION_HISTORY))
    .row(types.KeyboardButton(text.MENU))
)


def get_trips_pagination_keyboard(previous_callback_data: str = "previous", next_callback_data: str = "next"):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton("<<", callback_data=previous_callback_data),
        types.InlineKeyboardButton(">>", callback_data=next_callback_data),
    )
