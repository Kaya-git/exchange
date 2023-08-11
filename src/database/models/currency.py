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
    tikker: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True,
    )
