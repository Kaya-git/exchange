from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
import sqlalchemy as sa
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .payment_opt import PaymentOption


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True,
    )
    tikker_id: Mapped[int] = mapped_column(
        sa.Integer,
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
        default=0,
    )
    max: Mapped[int] = mapped_column(
        sa.Integer,
        default=0,
    )

    payment_options: Mapped[List["PaymentOption"]] = relationship(
        back_populates="currency"
    )

    def __str__(self) -> str:
        return self.tikker
