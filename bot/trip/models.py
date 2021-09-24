from sqlalchemy import Column, Integer, DateTime, Table, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from bot.core.db import Base
from bot.user.models import User

trips_users = Table(
    'trips_users',
    Base.metadata,
    Column('user', ForeignKey('users.id'), primary_key=True),
    Column('trip', ForeignKey('trips.id'), primary_key=True)
)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    users = relationship(User, secondary=trips_users)
    creator = Column(Integer, ForeignKey("users.id"))
    distance = Column(Float)
    cost = Column(Float)
    auto = Column(Integer, ForeignKey("autos.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}
