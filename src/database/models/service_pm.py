from .base import Base
from .currency import Currency
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa


class ServicePM(Base):
    __tablename__ = "service_pm"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    currency_id: Mapped[int] = mapped_column(
        sa.ForeignKey("currency.id")
    )
    currency: Mapped[Currency] = relationship(
        back_populates="service_pm",
        uselist=True,
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
