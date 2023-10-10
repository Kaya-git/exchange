from .base import Base
from .role import Role
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .review import Review
    from .payment_option import PaymentOption
    from .order import Order


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True
    )
    email: Mapped[str] = mapped_column(
        sa.String(length=320),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        sa.Text,
        nullable=True,
    )
    second_name: Mapped[str] = mapped_column(
        sa.Text,
        nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(
        sa.String(length=1024),
        nullable=True,
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
    buy_volume: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
        default=None,
        nullable=True,
    )
    role: Mapped["Role"] = mapped_column(
        sa.Enum(Role),
        default=Role.User
    )

    reviews: Mapped[List["Review"]] = relationship()
    payment_options: Mapped[List["PaymentOption"]] = relationship()
    orders: Mapped[List["Order"]] = relationship()
