from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa


class Commissions(Base):
    __tablename__ = "commissions"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    margin: Mapped[float] = mapped_column(
        sa.Float,
        default=7,
        nullable=False,
    )
    gas: Mapped[float] = mapped_column(
        sa.Float,
        default=130,
        nullable=False,
    )
