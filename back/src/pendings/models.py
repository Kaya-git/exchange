from database.base_model import Base
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from enums.models import ReqAction
from typing import TYPE_CHECKING
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
    order_id: Mapped[int] = mapped_column(
        sa.ForeignKey("order.id"),
        nullable=True
    )
    review_id: Mapped[int] = mapped_column(
        sa.ForeignKey("review.id"),
        nullable=True
    )

    order: Mapped["Order"] = relationship(
        "Order",
        foreign_keys="[PendingAdmin.order_id]"
    )
    review: Mapped["Review"] = relationship(
        back_populates="pending_admin"
    )
