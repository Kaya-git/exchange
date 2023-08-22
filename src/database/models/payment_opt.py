from .base import Base
from .currency import Currency
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa


class PaymentOption(Base):
    __tablename__ = "payment_option"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    currency: Mapped[Currency] = mapped_column(
        sa.ForeignKey("currency.tikker")
    )
    sum: Mapped[float] = mapped_column(
        sa.Float,
        nullable=False,
    )
    cc_num: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=False,
    )
    cc_holder: Mapped[str] = mapped_column(
        sa.Text,
        unique=False,
        nullable=True
    )
    image_name: Mapped[str] = mapped_column(
        sa.Text,
        nullable=True
    )
