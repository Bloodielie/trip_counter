from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DEBUG = bool(os.environ.get("DEBUG"))
