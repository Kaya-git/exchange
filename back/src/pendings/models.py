from typing import TYPE_CHECKING

import sqlalchemy as sa
from database.base_model import Base
from enums.models import ReqAction
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
        sa.ForeignKey("order.id", ondelete="CASCADE"),
        unique=True
    )
    review_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("review.id", ondelete="CASCADE"),
        unique=True
    )

    order: Mapped["Order"] = relationship(
        back_populates="pending_admin",
        passive_deletes=True
    )
    review: Mapped["Review"] = relationship(
        back_populates="pending_admin",
        passive_deletes=True
    )
