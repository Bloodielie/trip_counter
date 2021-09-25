from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from bot.core.config import DEBUG

Base = declarative_base()

engine = create_async_engine("sqlite+aiosqlite:///../trip_db.db", echo=DEBUG)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
