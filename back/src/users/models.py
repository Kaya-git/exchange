from database.base_model import Base
from enums import Role
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from reviews import Review
    from payment_options import PaymentOption
    from orders import Order


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    email: Mapped[str] = mapped_column(
        sa.String(length=320),
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

    payment_options: Mapped[List["PaymentOption"]] = relationship(
        back_populates="user",
    )
    reviews: Mapped[List["Review"]] = relationship(
        back_populates="user"
    )
    # orders: Mapped[List["Order"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        return f"{self.email}"

    def __repr__(self) -> str:
        return f"{self.email}"
