from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from decimal import Decimal


class OrderBase(BaseModel):
    user_email: int
    user_cookie: str
    user_buy_sum: Decimal
    user_sell_sum: Decimal
    status: Enum
    sell_payment_option_id: int
    buy_payment_option_id: int
    service_sell_po_id: int
    service_buy_po_id: int
    user_id: int
    sell_currency_id: str
    buy_currency_id: str

class OrderCreate(OrderBase):
    ...

class Order(OrderBase):
    id: int
    date: datetime

    class Config:
        orm_mmode = True