from .base import Base
from .mark import Mark
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user_email: Mapped[str] = mapped_column(
        sa.ForeignKey("user.email")
    )
    text: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False
    )
    data: Mapped[int] = mapped_column(
        sa.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )
    rating: Mapped[Mark] = mapped_column(
        sa.Enum(Mark)
    )