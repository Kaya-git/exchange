from .base import Base
from .banking_type import BankingType
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class ServicePaymentOption(Base):
    __tablename__ = "service_payment_option"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    banking_type: Mapped[BankingType] = mapped_column(
        sa.Enum(BankingType)
    )
    currency_id: Mapped[str] = mapped_column(
        sa.ForeignKey("currency.id")
    )
    number: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True
    )
    holder: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False
    )
