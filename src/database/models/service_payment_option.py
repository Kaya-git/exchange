from .base import Base
from .banking_type import BankingType
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .currency import Currency


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
    number: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True
    )
    holder: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False
    )

    currency_id: Mapped[int] = mapped_column(
        sa.ForeignKey("currency.id")
    )

    currency: Mapped["Currency"] = relationship(
        back_populates="service_payment_options"
    )

    def __repr__(self) -> str:
        return f"{self.currency_id}"

    def __str__(self) -> str:
        return f"{self.currency_id}"
