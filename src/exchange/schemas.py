from pydantic import BaseModel
from database.models import (
    Currency, Order,
    PaymentOption, Review,
    ServicePaymentOption, User,
)
from enum import Enum
from datetime import datetime
from decimal import Decimal


class CurrencyBase(BaseModel):
    tikker_id: int
    tikker: str
    type: Enum
    name: str
    gas: Decimal
    service_margin: Decimal
    reserve: Decimal
    max: Decimal
    min: Decimal
    icon: str


class CurrencyCreate(CurrencyBase):
    ...


class Currency(CurrencyBase):
    id: int

    class Config:
        orm_mode = True


# --------------------------------------------------
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

class CurrencyCreate(CurrencyBase):
    ...

class Currency(CurrencyBase):
    id: int
    date: datetime

    class Config:
        orm_mmode = True


# --------------------------------------------------
class PaymentOptionBase(BaseModel):
    banking_type: Enum
    number: str
    holder: str
    is_verified: bool
    image: str
    user_id: int
    currency_id: int

class PaymentOptionCreate(PaymentOptionBase):
    ...

class PaymentOption(PaymentOptionBase):
    id: int


# --------------------------------------------------
class ReviewBase(BaseModel):
    text: str
    rating: Enum
    user_id: int

class ReviewCreation(ReviewBase):
    ...

class Review(ReviewBase):
    id: int
    data: datetime


# --------------------------------------------------
class ServicePaymentOptionBase(BaseModel):
    banking_type: Enum
    number: str
    holder: str
    currency_id: int

class ServicePaymentOptionCreation(ServicePaymentOptionBase):
    ...

class ServicePaymentOption(ServicePaymentOptionBase):
    id: int


# --------------------------------------------------
class UserBase(BaseModel):
    email: str
    first_name: str
    second_name: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    buy_volume: Decimal
    role: Enum

class UserCreation(UserBase):
    ...

class User(UserBase):
    id: int
    registered_on: datetime
