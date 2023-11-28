from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import Base
from enums.models import ReqAction

if TYPE_CHECKING:
    from orders.models import Order
    from reviews.models import Review


class PendingAdmin(Base):
    __tablename__ = "pending_admin"

    id: Mapped[int] = mapped_column(
        sa.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    req_act: Mapped[ReqAction] = mapped_column(
        sa.Enum(ReqAction),
        default=None,
        nullable=True
    )
    order_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("order.id"),
        unique=True
    )
    review_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("review.id"),
        unique=True
    )

    order: Mapped["Order"] = relationship(
        back_populates="pending_admin"
    )
    review: Mapped["Review"] = relationship(
        back_populates="pending_admin"
    )
