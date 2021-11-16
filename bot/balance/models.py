from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, Boolean
from sqlalchemy.sql import func

from bot.settings.db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(Numeric(precision=15, scale=6, asdecimal=True))
    sender = Column(Integer, ForeignKey("users.id"), nullable=True)
    receiver = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True, index=True)

    __mapper_args__ = {"eager_defaults": True}
