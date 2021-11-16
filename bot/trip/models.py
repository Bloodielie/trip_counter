from sqlalchemy import Column, Integer, DateTime, Table, ForeignKey, Float, String, Numeric, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from bot.settings.db import Base
from bot.user.models import User

trips_users = Table(
    "trips_users",
    Base.metadata,
    Column("passenger", Integer, ForeignKey("users.id")),
    Column("trip", Integer, ForeignKey("trips.id")),
    PrimaryKeyConstraint('passenger', 'trip')
)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    passengers = relationship(User, secondary=trips_users)
    driver = Column(Integer, ForeignKey("users.id"), unique=False, index=True)
    distance = Column(Float)
    cost = Column(Numeric(precision=15, scale=6, asdecimal=True))
    auto = Column(Integer, ForeignKey("autos.id"), index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False, index=True)

    __mapper_args__ = {"eager_defaults": True}


class Auto(Base):
    __tablename__ = "autos"

    id = Column(Integer, primary_key=True)
    multiplier = Column(Float)
    consumption = Column(Float)
    identifier = Column(String(150), index=True)
    owner = Column(Integer, ForeignKey("users.id"))
    fuel = Column(Integer, ForeignKey("fuels.id"), index=True)


class Fuel(Base):
    __tablename__ = "fuels"

    id = Column(Integer, primary_key=True)
    price = Column(Numeric(precision=15, scale=6, asdecimal=True))
    identifier = Column(String(150), unique=True, index=True)
