from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from typing import TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from .pending_order import PendingOrder


class PaymentBelonging(enum.StrEnum):
    Client = "client"
    Service = "service"


class PaymentPointer(enum.StrEnum):
    From = "from"
    To = "to"


class PaymentOption(Base):
    __tablename__ = "payment_option"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    cc_num_x_wallet: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )
    cc_holder: Mapped[str] = mapped_column(
        sa.Text,
        unique=False,
        default=None,
        nullable=True
    )
    image_name: Mapped[str] = mapped_column(
        sa.Text,
        default=None,
        nullable=True
    )
    payment_point: Mapped[PaymentPointer] = mapped_column(
        sa.Enum(PaymentPointer),
    )
    clien_service_belonging: Mapped[PaymentBelonging] = mapped_column(
        sa.Enum(PaymentBelonging),
    )

    currency_id: Mapped[int] = mapped_column(
        sa.ForeignKey("currency.id"),
        nullable=True,
    )
    pending_order_id: Mapped[int] = mapped_column(
        sa.ForeignKey("pending_order.id"),
        nullable=True,
        default=None,
    )
    completed_order_id: Mapped[int] = mapped_column(
        sa.ForeignKey("completed_order.id"),
        nullable=True,
        default=None,
    )

    pending_order: Mapped["PendingOrder"] = relationship(
        back_populates="payment_options",
        uselist=True,
    )
