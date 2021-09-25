from typing import List, Iterable

from aiogram import types

from bot.shared import text
from bot.shared.utils import parting

back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(types.KeyboardButton(text.BACK))


def get_user_keyboard(usernames: Iterable[str]) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    usernames_chunks = parting(usernames, 4)
    for chunk in usernames_chunks:
        if not len(chunk):
            break

        keyboard.row(*[types.KeyboardButton(username) for username in chunk])

    keyboard.row(types.KeyboardButton(text.MENU))

    return keyboard
