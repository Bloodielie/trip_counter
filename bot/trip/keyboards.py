from typing import List

from aiogram import types

from bot.auto.models import Auto
from bot.core import text
from bot.core.utils import parting
from bot.user.models import User

select_distance_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(types.KeyboardButton(text.MENU))
confirm_trip_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(
    types.KeyboardButton(text.CONFIRM), types.KeyboardButton(text.CANCEL)
)


def get_users_keyboard(users: List[User]) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    users_chunks = parting(users, 4)
    for chunk in users_chunks:
        if not len(chunk):
            break

        keyboard.row(*[types.KeyboardButton(user.name) for user in chunk])

    keyboard.row(types.KeyboardButton(text.BACK), types.KeyboardButton(text.COMPLETE))

    return keyboard


def get_autos_keyboard(autos: List[Auto]) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    chunks = parting(autos, 4)
    for chunk in chunks:
        if not len(chunk):
            break

        keyboard.row(*[types.KeyboardButton(auto.identifier) for auto in chunk])

    keyboard.row(types.KeyboardButton(text.BACK))

    return keyboard
