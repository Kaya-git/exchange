from .base import Base
from .currency import Currency
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa


class PaymentOption(Base):
    __tablename__ = "paymentoptions"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=False,
    )
    currency: Mapped[Currency] = mapped_column(
        sa.ForeignKey("currency.tikker")
    )
    banking_acc_number: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=False,
    )
