from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DEBUG = bool(os.environ.get("DEBUG"))

ADMIN_TELEGRAM_ID = 419122895
ADMIN_NAME = "Рома"

AUTO_1_IDENTIFIER = "Peugeot 307"
AUTO_1_FUEL_PRICE = 2.07
AUTO_1_CONSUMPTION = 7.20
AUTO_1_MULTIPlIER = 1.05
