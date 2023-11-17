from database.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa


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
