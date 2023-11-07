from pydantic import BaseModel
from enums import CryptoType
from datetime import datetime
from decimal import Decimal


class CurrencyBase(BaseModel):
    tikker_id: int
    tikker: str
    type: CryptoType
    name: str
    gas: Decimal
    service_margin: Decimal
    reserve: Decimal
    max: Decimal
    min: Decimal
    icon: str

class CurrencyCreate(CurrencyBase):
    ...

class CurrencyRead(CurrencyBase):
    id: int

    class Config:
        orm_mode = True

class CurrencyTariffsRead(BaseModel):
    id: int
    name: str
    tikker: str
    icon: str
    reserve: Decimal
    max: Decimal
    min: Decimal
    coin_price: Decimal

    class Config:
        orm_mode = True
