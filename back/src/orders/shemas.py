from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr

from enums import Status, VerifDeclineReason


class OrderBase(BaseModel):
    buy_payment_option_id: int
    decline_reason: VerifDeclineReason | None
    service_buy_po_id: int | None
    sell_payment_option_id: int
    user_id: int
    sell_currency_id: int
    user_buy_sum: Decimal
    buy_currency_id: int
    user_sell_sum: Decimal
    user_email: EmailStr
    user_cookie: str
    date: datetime
    status: Status
    service_sell_po_id: Optional[int]


class OrderCreate(OrderBase):
    ...


class OrderRead(OrderBase):
    id: int

    class Config:
        from_attributes = True
