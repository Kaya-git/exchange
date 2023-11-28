
from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import conf
from database.base_model import Base
from enums import CurrencyType

if TYPE_CHECKING:
    from payment_options.models import PaymentOption
    from service_payment_options.models import ServicePaymentOption


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
    )
    coingecko_tik: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )
    tikker: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=False,
    )
    type: Mapped[CurrencyType] = mapped_column(
        sa.Enum(CurrencyType)
    )
    name: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=False
    )
    buy_gas: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
        default=130,
        nullable=False
    )
    buy_margin: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
        default=7,
        nullable=False
    )
    reserve: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
        default=0,
    )
    max: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
        default=0,
    )
    min: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
        default=0,
    )
    icon: Mapped[str] = mapped_column(
        FileType(storage=conf.image_admin_storage),
        nullable=True
    )

    service_payment_options: Mapped[
        List["ServicePaymentOption"]
    ] = relationship(
        back_populates="currency"
    )
    payment_options: Mapped[
        List["PaymentOption"]
    ] = relationship(
        back_populates="currency"
    )

    def __repr__(self) -> str:
        return f"{self.tikker}"

    def __str__(self) -> str:
        return f"{self.tikker}"
