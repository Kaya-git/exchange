import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from database.base_model import Base


class Contact(Base):
    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True
    )
    link: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
        unique=True
    )
