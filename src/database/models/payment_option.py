from .base import Base
from .banking_type import BankingType
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .currency import Currency
    from .user import User


class PaymentOption(Base):
    __tablename__ = "payment_option"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    banking_type: Mapped[BankingType] = mapped_column(
        sa.Enum(BankingType)
    )
    currency_id: Mapped[int] = mapped_column(
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
    is_verified: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False
    )
    image: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id")
    )
    currency_id: Mapped[int] = mapped_column(
        sa.ForeignKey("currency.id")
    )

    currency: Mapped["Currency"] = relationship(
        back_populates="payment_options"
    )
    user: Mapped["User"] = relationship(
        back_populates="payment_options"
    )

    def __str__(self) -> str:
        return f"{self.banking_type}"

    def __repr__(self) -> str:
        return f"{self.banking_type}"
