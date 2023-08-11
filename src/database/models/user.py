from .base import Base
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTable
import enum


class Role(enum.IntEnum):
    User = 1
    Moderator = 2
    Admin = 3


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user_name: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        sa.String(length=320),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        sa.String(length=1024),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False,
        nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False,
        nullable=False,
    )
    registered_on: Mapped[int] = mapped_column(
        sa.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )
    role: Mapped[Role] = mapped_column(
        sa.Enum(Role),
        default=Role.User
    )
