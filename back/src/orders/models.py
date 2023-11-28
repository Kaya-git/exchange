from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import Base
from enums import Status, VerifDeclineReason

if TYPE_CHECKING:
    from currencies.models import Currency
    from payment_options.models import PaymentOption
    from service_payment_options.models import ServicePaymentOption
    from users.models import User
    from pendings.models import PendingAdmin


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user_email: Mapped[str] = mapped_column(
        sa.ForeignKey("user.email")
    )
    user_cookie: Mapped[str] = mapped_column(
        sa.Text,
        default=None
    )
    user_buy_sum: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
    )

    user_sell_sum: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
    )
    date: Mapped[int] = mapped_column(
        sa.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )
    status: Mapped["Status"] = mapped_column(
        sa.Enum(Status)
    )
    decline_reason: Mapped["VerifDeclineReason"] = mapped_column(
        sa.Enum(VerifDeclineReason),
        nullable=True
    )

    sell_payment_option_id: Mapped[int] = mapped_column(
        sa.ForeignKey("payment_option.id")
    )
    buy_payment_option_id: Mapped[int] = mapped_column(
        sa.ForeignKey("payment_option.id")
    )
    service_sell_po_id: Mapped[int] = mapped_column(
        sa.ForeignKey("service_payment_option.id"),
        nullable=True
    )
    service_buy_po_id: Mapped[int] = mapped_column(
        sa.ForeignKey("service_payment_option.id"),
        nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id", ondelete="CASCADE")
    )
    sell_currency_id: Mapped[str] = mapped_column(
        sa.ForeignKey("currency.id", ondelete="CASCADE")
    )
    buy_currency_id: Mapped[str] = mapped_column(
        sa.ForeignKey("currency.id", ondelete="CASCADE")
    )

    sell_payment_option: Mapped["PaymentOption"] = relationship(
        "PaymentOption",
        foreign_keys="[Order.sell_payment_option_id]"
    )
    buy_payment_option: Mapped["PaymentOption"] = relationship(
        "PaymentOption",
        foreign_keys="[Order.buy_payment_option_id]"
    )
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys="Order.user_id"
    )
    service_sell_po: Mapped["ServicePaymentOption"] = relationship(
        "ServicePaymentOption",
        foreign_keys="[Order.service_sell_po_id]"
    )
    service_buy_po: Mapped["ServicePaymentOption"] = relationship(
        "ServicePaymentOption",
        foreign_keys="[Order.service_buy_po_id]"
    )
    sell_currency: Mapped["Currency"] = relationship(
        "Currency",
        foreign_keys="[Order.sell_currency_id]"
    )
    buy_currency: Mapped["Currency"] = relationship(
        "Currency",
        foreign_keys="[Order.buy_currency_id]"
    )
    pending_admin: Mapped["PendingAdmin"] = relationship(
        back_populates="order"
    )

    def __str__(self) -> str:
        return f"{self.id}"

    def __repr__(self) -> str:
        return f"{self.id}"
