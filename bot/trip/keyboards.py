from typing import List

from aiogram import types

from bot.auto.models import Auto
from bot.shared import text
from bot.shared.utils import parting
from bot.user.models import User

select_distance_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(types.KeyboardButton(text.MENU))
confirm_trip_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(
    types.KeyboardButton(text.CONFIRM), types.KeyboardButton(text.CANCEL)
)


def get_users_keyboard(users: List[User], ignore_user: User) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    users_chunks = parting(users, 4)
    for chunk in users_chunks:
        if not len(chunk):
            break

        keyboard.row(*[types.KeyboardButton(user.name) for user in chunk if user.id != ignore_user.id])

    keyboard.row(types.KeyboardButton(text.BACK), types.KeyboardButton(text.COMPLETE))

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
