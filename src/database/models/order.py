from .base import Base
import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped, relationship
import datetime
from .order_status import Status
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .payment_opt import PaymentOption
    from .currency import Currency


class CompletedOrder(Base):
    __tablename__ = "completed_order"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    email: Mapped[str] = mapped_column(
        sa.String,
        nullable=False,
    )
    give_amount: Mapped[float] = mapped_column(
        sa.Float,
        nullable=False,
    )
    get_amount: Mapped[float] = mapped_column(
        sa.Float,
        nullable=False,
    )
    date: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow(),
    )
    status: Mapped[Status] = mapped_column(
        sa.Enum(Status),
        default=Status.InProcess,
    )
    user_uuid: Mapped[str] = mapped_column(
        sa.String,
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id"),
        nullable=True
    )
    give_currency_id: Mapped[int] = mapped_column(
        sa.ForeignKey("currency.id"),
        nullable=True
    )
    get_currency_id: Mapped[int] = mapped_column(
        sa.ForeignKey("currency.id"),
    )

    give_currency: Mapped["Currency"] = relationship(
        "Currency",
        foreign_keys="[CompletedOrder.give_currency_id]",
    )
    get_currency: Mapped["Currency"] = relationship(
        "Currency",
        foreign_keys="[CompletedOrder.get_currency_id]",
    )
    payment_options: Mapped[List["PaymentOption"]] = relationship(
    )
