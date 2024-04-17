from typing import TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import Base

if TYPE_CHECKING:
    from pendings.models import PendingAdmin


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        sa.String(30),
        nullable=False
    )
    text: Mapped[str] = mapped_column(
        sa.String(250),
        nullable=False
    )
    rating: Mapped[int] = mapped_column(
        sa.SmallInteger,
        nullable=False
    )
    date: Mapped[int] = mapped_column(
        sa.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )
    moderated: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False
    )

    pending_admin: Mapped["PendingAdmin"] = relationship(
        back_populates="review",
        passive_deletes=True
    )

    def __str__(self) -> str:
        return f"{self.id}"

    def __repr__(self) -> str:
        return f"{self.id}"
