from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import Base
from enums.models import ReqAction

if TYPE_CHECKING:
    from orders.models import Order
    from reviews.models import Review
    from payment_options.models import PaymentOption


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
        sa.ForeignKey("order.id", ondelete="CASCADE")
    )
    review_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("review.id", ondelete="CASCADE")
    )
    payment_option_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("payment_option.id", ondelete="CASCADE")
    )

    order: Mapped["Order"] = relationship(
        back_populates="pending_admin",
        passive_deletes=True
    )
    review: Mapped["Review"] = relationship(
        back_populates="pending_admin",
        passive_deletes=True
    )
    payment_option: Mapped["PaymentOption"] = relationship(
        back_populates="pending_admin",
        passive_deletes=True
    )
