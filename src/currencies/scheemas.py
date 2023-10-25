from pydantic import BaseModel
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
