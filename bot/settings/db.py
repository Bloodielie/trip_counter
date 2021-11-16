from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from bot.settings.config import DEBUG, DATABASE_URL

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=DEBUG, enable_from_linting=DEBUG, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)
