from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.sql import func

from bot.core.db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)

    __mapper_args__ = {"eager_defaults": True}
