from logging import getLogger

from aiogram.dispatcher.handler import CancelHandler

logger = getLogger(__name__)


async def errors_handler(update, exception):
    if isinstance(exception, CancelHandler):
        return None

    logger.exception("Update: %s \n%s", update, exception)
