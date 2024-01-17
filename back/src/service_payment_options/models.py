from typing import TYPE_CHECKING

import sqlalchemy as sa
from database.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from currencies.models import Currency


class ServicePaymentOption(Base):
    __tablename__ = "service_payment_option"

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

    currency_id: Mapped[int] = mapped_column(
        sa.ForeignKey("currency.id", ondelete="CASCADE")
    )

    currency: Mapped["Currency"] = relationship(
        back_populates="service_payment_options",
        lazy="joined",
        single_parent=True
    )

    def __repr__(self) -> str:
        return f"{self.currency_id}"

    def __str__(self) -> str:
        return f"{self.currency_id}"
