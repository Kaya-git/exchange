from .base import Base
from .currency import Currency
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa


class ServicePM(Base):
    __tablename__ = "service_pm"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    currency: Mapped[Currency] = mapped_column(
        sa.ForeignKey("currency.tikker")
    )

    cc_num_x_wallet: Mapped[str] = mapped_column(
        sa.Text,
        unique=True,
        nullable=False,
    )
    cc_holder: Mapped[str] = mapped_column(
        sa.Text,
        unique=False,
        default=None
    )
