from sqlalchemy import Column, Integer, DateTime, Table, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from bot.db import Base
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
    date = Column(DateTime(timezone=True), server_default=func.now())
    users = relationship(User, secondary=trips_users)
