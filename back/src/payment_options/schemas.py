from pydantic import BaseModel
from enum import Enum


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

class PaymentOptionRead(PaymentOptionBase):
    id: int

    class Config:
        from_attributes = True
