from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from .user import User
import datetime
import enum


class Mark(enum.StrEnum):
    Good = "good"
    Bad = "bad"


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        autoincrement=True,
        primary_key=True,
    )
    author: Mapped[User] = mapped_column(
        sa.ForeignKey("user.id")
    )
    text: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False
    )
    data: Mapped[datetime.date] = mapped_column(
        sa.Date,
        nullable=False,
        default=datetime.date.today()
    )
    mark: Mapped[Mark] = mapped_column(
        sa.Enum(Mark),
        default=Mark.Good,
    )
