from typing import List

from aiogram import types

from bot.core import text
from bot.core.utils import parting
from bot.user.models import User

back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(types.KeyboardButton(text.BACK))


def get_user_keyboard(users: List[User]) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    users_chunks = parting(users, 4)
    for chunk in users_chunks:
        if not len(chunk):
            break

        keyboard.row(*[types.KeyboardButton(user.name) for user in chunk])

    keyboard.row(types.KeyboardButton(text.MENU))

    return keyboard
