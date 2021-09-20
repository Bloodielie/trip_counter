from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from bot.config import DEBUG


engine = create_async_engine("sqlite+aiosqlite:///../trip_db.db", echo=DEBUG)
Base = declarative_base()
