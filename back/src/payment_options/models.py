from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import Base

if TYPE_CHECKING:
    from currencies.models import Currency
    from users.models import User
    from pendings.models import PendingAdmin


class PaymentOption(Base):
    __tablename__ = "payment_option"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
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
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True
    )
    currency_id: Mapped[int] = mapped_column(
        sa.ForeignKey("currency.id", ondelete="CASCADE"),
        nullable=True
    )

    currency: Mapped["Currency"] = relationship(
        back_populates="payment_options",
        single_parent=True
    )
    user: Mapped["User"] = relationship(
        back_populates="payment_options"
    )
    pending_admin: Mapped["PendingAdmin"] = relationship(
        back_populates="payment_option",
        passive_deletes=True
    )

    def __str__(self) -> str:
        return f"{self.id}"

    def __repr__(self) -> str:
        return f"{self.id}"
