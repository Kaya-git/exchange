from database.base_model import Base
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enums import CryptoType
from config import conf
from fastapi_storages.integrations.sqlalchemy import ImageType
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from service_payment_options import ServicePaymentOption
    from payment_options import PaymentOption


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
    )
    tikker_id: Mapped[int] = mapped_column(
        sa.SmallInteger,
        unique=True,
        nullable=False,
    )
    tikker: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=False,
    )
    type: Mapped[CryptoType] = mapped_column(
        sa.Enum(CryptoType)
    )
    name: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=False
    )
    gas: Mapped[sa.Numeric] = mapped_column(
        sa.Numeric,
        default=130,
        nullable=False
    )
    service_margin: Mapped[sa.Numeric] = mapped_column(
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
        ImageType(storage=conf.image_admin_storage),
        default=None,
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
