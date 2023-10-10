from .base import Base
from .status import Status
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


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
    buy_currency_tikker: Mapped[str] = mapped_column(
        sa.ForeignKey("currency.tikker")
    )
    buy_payment_option: Mapped[int] = mapped_column(
        sa.ForeignKey("payment_option.id")
    )
    user_sell_sum: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
    )
    sell_currency_tikker: Mapped[str] = mapped_column(
        sa.ForeignKey("currency.tikker")
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
