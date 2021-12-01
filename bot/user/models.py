from sqlalchemy import Column, Integer, String, Numeric, Table, ForeignKey, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import relationship

from bot.settings.db import metadata, Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    balance = Column(Numeric(precision=15, scale=6, asdecimal=True), default=0)
    identifier = Column(String(250), nullable=True, unique=True, index=True)
    roles = relationship("Role", "users_roles")


users_roles = Table(
    "users_roles",
    metadata,
    Column("user", Integer, ForeignKey("users.id")),
    Column("role", Integer, ForeignKey("roles.id")),
    PrimaryKeyConstraint('user', 'role')
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    codename = Column(String(64), unique=True, nullable=False, index=True)
    description = Column(String(256), nullable=True)


class Invite(Base):
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True)
    creator = Column(Integer, ForeignKey("users.id"))
    invited = Column(Integer, ForeignKey("users.id"), nullable=True)
    hash = Column(String(64), nullable=False, index=True)
    user_identifier = Column(String(32), unique=True)
