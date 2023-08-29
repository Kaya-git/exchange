from pydantic import BaseModel
from database.models import (
    User, PaymentOption,
    Status, Currency,
    PendingStatus, Mark,
)
import datetime


class CommissionsBase(BaseModel):
    margin: float
    gas: float


class CommissionsCreate(CommissionsBase):
    ...


class Commissions(CommissionsBase):
    id: int

    class Config:
        orm_mode = True


# --------------------------------------------------
class CurrencyBase(BaseModel):
    name: str
    tikker: str
    reserve: float
    min: int
    max: int


class CurrencyCreate(CurrencyBase):
    ...


class CurrencyRead(CurrencyBase):
    id: int

    class Config:
        orm_mmode = True


# --------------------------------------------------
class OrderBase(BaseModel):
    user: User.id
    payment_from: PaymentOption.id
    payment_to: PaymentOption.id
    date: datetime.datetime
    status: Status


class OrderCreate(OrderBase):
    ...


class OrderRead(OrderBase):
    id: int

    class Config:
        orm_mode = True


# --------------------------------------------------
class PaymentOptionBase(BaseModel):
    currency: Currency.tikker
    amount: float
    cc_num_x_wallet: str
    cc_holder: str
    image_name: str


class PaymentOptionCreate(PaymentOptionBase):
    ...


class PaymentOptionRead(PaymentOptionBase):
    id: int

    class Config:
        orm_mode = True


# --------------------------------------------------
class PendingOrderBase(BaseModel):
    email: str
    payment_from: PaymentOption.id
    payment_to: PaymentOption.id
    date: datetime.datetime
    status: PendingStatus
    user_uuid: str


class PendingOrderCreate(PendingOrderBase):
    ...


class PendingOrderRead(PendingOrderBase):
    id: int

    class Config:
        orm_mode = True


# --------------------------------------------------
class ReviewBase(BaseModel):
    author: User.id
    text: str
    data: datetime.date
    mark: Mark


class ReviewCreate(ReviewBase):
    ...


class ReviewRead(ReviewBase):
    id: int

    class Config:
        orm_mode = True
