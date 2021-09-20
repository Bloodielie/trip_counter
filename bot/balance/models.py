from sqlalchemy import Column, Integer, DateTime, BigInteger, ForeignKey
from sqlalchemy.sql import func

from bot.db import Base


class Deposit(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    deposit = Column(BigInteger)


class Balance(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"))
    current = Column(BigInteger)
    difference = Column(BigInteger)
    date = Column(DateTime(timezone=True), server_default=func.now())
