from .base import Base
import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped
import datetime
from .order_status import PendingStatus


class PendingOrder(Base):
    __tablename__ = "pending_order"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    email: Mapped[str] = mapped_column(
        sa.String,
        nullable=False,
    )
    get_value: Mapped[float] = mapped_column(
        sa.Float,
        nullable=False
    )
    send_value: Mapped[float] = mapped_column(
        sa.Float,
        nullable=False
    )
    cc_num: Mapped[int] = mapped_column(
        sa.BigInteger,
        nullable=False
    )
    cc_holder: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )
    cc_image_name: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False
    )
    date: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow(),
    )
    status: Mapped[PendingStatus] = mapped_column(
        sa.Enum(PendingStatus),
        default=PendingStatus.InProcess,
    )
