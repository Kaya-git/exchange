from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from .currency import Currency
from .user import User
import sqlalchemy as sa


class CWallet(Base):
    __tablename__ = "crypto_wallets"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user: Mapped[User] = mapped_column(
        sa.ForeignKey("user.id")
    )
    currency: Mapped[Currency] = mapped_column(
        sa.ForeignKey("currency.name")
    )
    num: Mapped[str] = mapped_column(
        sa.Text,
        unique=False,
        nullable=False,
    )


class EWallets(Base):
    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user: Mapped[User] = mapped_column(
        sa.ForeignKey("user.id")
    )
    currency: Mapped[Currency] = mapped_column(
        sa.ForeignKey("currency.name")
    )
    num: Mapped[str] = mapped_column(
        sa.Text,
        unique=False,
        nullable=False,
    )
