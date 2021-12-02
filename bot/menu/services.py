from typing import List

from bot.balance.models import Transaction
from bot.menu.text import USER_TRANSACTION, USER_TRIP
from bot.trip.dto import TripInfo
from bot.user.models import User


def formatting_trips(user: User, trips: List[TripInfo]) -> str:
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
    return "\n".join(
        [
            USER_TRANSACTION.format(
                transaction.date.astimezone().strftime("%H:%M:%S %B %d, %Y"),
                "отправил" if transaction.sender == user.id else "получил",
                transaction.amount,
            )
            for transaction in transactions
        ]
    )
