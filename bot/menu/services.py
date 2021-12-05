from typing import List

import pymorphy2

from bot.balance.models import Transaction
from bot.menu.text import USER_TRANSACTION, USER_TRIP, USER__ADD_BALANCE_TRANSACTION
from bot.trip.dto import TripInfo
from bot.user.models import User

morph = pymorphy2.MorphAnalyzer()


def convert_word_to_case(word: str, case: str) -> str:
    return morph.parse(word)[0].inflect({case}).word


def formatting_trips(_: User, trips: List[TripInfo]) -> str:
    return "\n".join(
        USER_TRIP.format(
            distance=trip.distance,
            date=trip.date.astimezone().strftime("%H:%M:%S %B %d, %Y"),
            auto_identifier=trip.auto_identifier,
            creator_name=trip.creator_name,
            passengers=", ".join(trip.passengers),
            cost=trip.cost,
        )
        for trip in trips
    )


def formatting_transactions(user: User, transactions: List[Transaction]) -> str:
    result = ""
    for transaction in transactions:
        date = transaction.date.astimezone().strftime("%H:%M:%S %B %d, %Y")

        if transaction.sender is None:
            result += USER__ADD_BALANCE_TRANSACTION.format(date, transaction.amount)
        elif transaction.sender == user.id:
            result += USER_TRANSACTION.format(
                date,
                "отправил",
                transaction.amount,
                convert_word_to_case(transaction.receiver_obj.identifier, "datv").capitalize()
            )
        else:
            result += USER_TRANSACTION.format(
                date,
                "получил",
                transaction.amount,
                f"от {convert_word_to_case(transaction.sender_obj.identifier, 'gent').capitalize()}"
            )
        result += "\n"

    return result
