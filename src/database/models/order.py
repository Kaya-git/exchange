from .base import Base
from .currency import Currency
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
        sa.ForeignKey("user.id")
    )
    ammount_get: Mapped[float] = mapped_column(
        sa.Float,
        nullable=False,
    )
    get_currency: Mapped[Currency] = mapped_column(
        sa.ForeignKey("currency.tikker")
    )
    ammount_give: Mapped[float] = mapped_column(
        sa.Float,
        nullable=False,
    )
    give_currency: Mapped[Currency] = mapped_column(
        sa.ForeignKey("currency.tikker")
    )
    payment_option: Mapped[PaymentOption] = mapped_column(
        sa.ForeignKey("payment_option.name")
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
