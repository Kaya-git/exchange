from .base import Base
from .payment_opt import PaymentOption
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from .user import User
import datetime
from .order_status import Status


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user: Mapped[User] = mapped_column(
        sa.ForeignKey("user.id"),
        default=None,
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
        default=datetime.datetime.utcnow()
    )
    status: Mapped[Status] = mapped_column(
        sa.Enum(Status),
        default=Status.Pending
    )
