from .base import Base
from .mark import Mark
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
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

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id")
    )

    user: Mapped["User"] = relationship(
        back_populates="reviews"
    )

    def __str__(self) -> str:
        return f"{self.rating}"

    def __repr__(self) -> str:
        return f"{self.rating}"
