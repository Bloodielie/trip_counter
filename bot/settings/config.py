from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DEBUG = bool(strtobool(os.environ.get("DEBUG")))
DATABASE_URL = os.environ.get("DATABASE_URL")

LIMIT_EVENTS_PER_MIN = 100

PATH_TO_STATES = os.path.join(Path(__file__).parent.parent, "user_states.json")

ADMIN_TELEGRAM_ID = 419122895
ADMIN_NAME = "Рома"

AUTO_1_IDENTIFIER = "Peugeot 307"
AUTO_1_CONSUMPTION = 7.20
AUTO_1_MULTIPlIER = 1.05

DIESEL_IDENTIFIER = "Дизель"
DIESEL_PRICE = "2.09"

PERMISSION_ADMIN_CODENAME = "admin"
PERMISSION_DRIVER_CODENAME = "driver"
PERMISSION_PASSENGER_CODENAME = "passenger"
