from bot.core.db import Base
from sqlalchemy import Column, Integer, String, Enum
from enum import IntEnum


class Permissions(IntEnum):
    DEFAULT = 1
    ADMIN = 2
    SUPER_ADMIN = 3


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String(250), nullable=True, unique=True, index=True)
    role = Column(Enum(Permissions), default=Permissions.DEFAULT)
