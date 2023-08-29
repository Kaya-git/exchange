from .base import Base
import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped
import datetime
from .order_status import PendingStatus
from .payment_opt import PaymentOption


class PendingOrder(Base):
    __tablename__ = "pending_order"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    email: Mapped[str] = mapped_column(
        sa.String,
        nullable=False,
    )
    payment_from: Mapped[PaymentOption] = mapped_column(
        sa.ForeignKey("payment_option.id")
    )
    payment_to: Mapped[PaymentOption] = mapped_column(
        sa.ForeignKey("payment_option.id")
    )
    date: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow(),
    )
    status: Mapped[PendingStatus] = mapped_column(
        sa.Enum(PendingStatus),
        default=PendingStatus.InProcess,
    )
    user_uuid: Mapped[str] = mapped_column(
        sa.String,
        nullable=False,
    )
