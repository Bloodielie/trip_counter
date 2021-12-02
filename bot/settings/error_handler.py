from logging import getLogger

logger = getLogger(__name__)


async def errors_handler(update, exception):
    logger.exception('Update: %s \n%s', update, exception)
