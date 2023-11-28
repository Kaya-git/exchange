from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import Base
from enums import Mark

if TYPE_CHECKING:
    from pendings.models import PendingAdmin
    from users.models import User


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
    moderated: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False
    )

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id")
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews"
    )
    pending_admin: Mapped["PendingAdmin"] = relationship(
        back_populates="review"
    )

    def __str__(self) -> str:
        return f"{self.rating}"

    def __repr__(self) -> str:
        return f"{self.rating}"
