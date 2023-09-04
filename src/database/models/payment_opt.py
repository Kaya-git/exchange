from .base import Base
from .currency import Currency
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .pending_order import PendingOrder


class PaymentOption(Base):
    __tablename__ = "payment_option"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    amount: Mapped[float] = mapped_column(
        sa.Float,
        nullable=False,
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
    user_id: Mapped[Optional[str]] = mapped_column(
        sa.Text,
        default=None,
        nullable=True,
    )

    currency_id: Mapped[Currency] = mapped_column(
        sa.ForeignKey("currency.id")
    )
    pay_from_id: Mapped["PendingOrder"] = mapped_column(
        sa.ForeignKey("pending_order.id"),
        nullable=True
    )
    pay_to_id: Mapped["PendingOrder"] = mapped_column(
        sa.ForeignKey("pending_order.id"),
        nullable=True
    )

    currency: Mapped["Currency"] = relationship(
        back_populates="payment_opt",
        uselist=False
    )
    pay_to: Mapped["PendingOrder"] = relationship(
        back_populates="payment_to",
        uselist=False
    )
    pay_from: Mapped["PendingOrder"] = relationship(
        back_populates="payment_from",
        uselist=False
    )
