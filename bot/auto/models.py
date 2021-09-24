from sqlalchemy import Column, Integer, String, Float

from bot.core.db import Base


class Auto(Base):
    __tablename__ = "autos"

    id = Column(Integer, primary_key=True)
    fuel_price = Column(Float)
    multiplier = Column(Float)
    consumption = Column(Float)
    identifier = Column(String(150), unique=True, index=True)
