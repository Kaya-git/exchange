from pydantic import BaseModel
from enum import Enum


class ServicePaymentOptionBase(BaseModel):
    banking_type: Enum
    number: str
    holder: str
    currency_id: int

class ServicePaymentOptionCreation(ServicePaymentOptionBase):
    ...

class ServicePaymentOption(ServicePaymentOptionBase):
    id: int
