from .base import Base
from .status import Status
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
    from .service_payment_option import ServicePaymentOption
    from .currency import Currency


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
    buy_payment_option: Mapped[int] = mapped_column(
        sa.ForeignKey("payment_option.id")
    )
    user_sell_sum: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
    )
    sell_payment_option: Mapped[int] = mapped_column(
        sa.ForeignKey("payment_option.id")
    )
    date: Mapped[int] = mapped_column(
        sa.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )
    status: Mapped["Status"] = mapped_column(
        sa.Enum(Status)
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
        sa.ForeignKey("user.id")
    )
    sell_currency_id: Mapped[str] = mapped_column(
        sa.ForeignKey("currency.id")
    )
    buy_currency_id: Mapped[str] = mapped_column(
        sa.ForeignKey("currency.id")
    )

    user: Mapped["User"] = relationship(
        "User",
        foreign_keys="[Order.user_id]"
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

    def __str__(self) -> str:
        return f"{self.id}"

    def __repr__(self) -> str:
        return f"{self.id}"