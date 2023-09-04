from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
import sqlalchemy as sa
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .payment_opt import PaymentOption
    from .service_pm import ServicePM


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True,
    )
    tikker: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True,
    )
    reserve: Mapped[float] = mapped_column(
        sa.Float,
        default=0,
    )
    min: Mapped[int] = mapped_column(
        sa.Integer,
        default=0
    )
    max: Mapped[int] = mapped_column(
        sa.Integer,
        default=0
    )

    payment_opt: Mapped["PaymentOption"] = relationship(
        back_populates="currency",
        uselist=False
    )
    service_pm: Mapped["ServicePM"] = relationship(
        back_populates="currency"
    )

    def __str__(self) -> str:
        return self.tikker
