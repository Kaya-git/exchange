from .base import Base
from .banking_type import BankingType
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


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
    currency_tikker: Mapped[str] = mapped_column(
        sa.ForeignKey("currency.tikker")
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
    user_email: Mapped[str] = mapped_column(
        sa.ForeignKey("user.email")
    )
