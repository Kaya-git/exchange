from .base import Base
from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy as sa


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
