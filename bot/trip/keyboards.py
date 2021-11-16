from typing import List

from aiogram import types

from bot.shared import text
from bot.shared.utils import parting

select_distance_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(types.KeyboardButton(text.MENU))
confirm_trip_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(
    types.KeyboardButton(text.CONFIRM), types.KeyboardButton(text.CANCEL)
)
back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(types.KeyboardButton(text.BACK))


def get_users_keyboard(users_identifiers: List[str]) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    users_chunks = parting(users_identifiers, 4)
    for chunk in users_chunks:
        if not len(chunk):
            break

        keyboard.row(*[types.KeyboardButton(user_identifier) for user_identifier in chunk])

    return keyboard


def get_choice_users_keyboard(users_identifiers: List[str]) -> types.ReplyKeyboardMarkup:
    keyboard = get_users_keyboard(users_identifiers)
    keyboard.row(types.KeyboardButton(text.BACK), types.KeyboardButton(text.COMPLETE))
    return keyboard


def get_users_menu_keyboard(users_identifiers: List[str]) -> types.ReplyKeyboardMarkup:
    keyboard = get_users_keyboard(users_identifiers)
    keyboard.row(types.KeyboardButton(text.MENU))
    return keyboard


def get_autos_keyboard(auto_identifiers: List[str]) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    chunks = parting(auto_identifiers, 4)
    for chunk in chunks:
        if not len(chunk):
            break

        keyboard.row(*[types.KeyboardButton(auto_identifier) for auto_identifier in chunk])

    keyboard.row(types.KeyboardButton(text.BACK))

    return keyboard
