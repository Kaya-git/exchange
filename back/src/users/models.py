import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import Base
from enums import Role

if TYPE_CHECKING:
    from orders.models import Order
    from payment_options.models import PaymentOption


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
        default=0,
        nullable=True,
    )
    sell_volume: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
        default=0,
        nullable=True
    )
    role: Mapped["Role"] = mapped_column(
        sa.Enum(Role),
        default=Role.Клиент
    )
    verification_token: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True
    )
    payment_options: Mapped[List["PaymentOption"]] = relationship(
        back_populates="user",
        cascade="all,delete"
    )

    def __str__(self) -> str:
        return f"{self.email}"

    def __repr__(self) -> str:
        return f"{self.email}"
