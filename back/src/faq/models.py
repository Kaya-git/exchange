import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from database.base_model import Base


class FAQ(Base):
    __tablename__ = "faq"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    question: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True
    )
    answer: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True
    )
