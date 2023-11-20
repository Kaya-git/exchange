from pydantic import BaseModel
from enums import CurrencyType
from decimal import Decimal
from typing import Optional

class CurrencyBase(BaseModel):
    tikker_id: int
    tikker: str
    type: CurrencyType
    name: str
    gas: Decimal
    service_margin: Decimal
    reserve: Decimal
    max: Decimal
    min: Decimal
    icon: Optional[str]

class CurrencyCreate(CurrencyBase):
    ...

class CurrencyRead(CurrencyBase):
    id: int

    class Config:
        from_attributes = True

class CurrencyTariffsRead(BaseModel):
    id: int
    name: str
    tikker: str
    icon: Optional[str]
    reserve: Decimal
    max: Decimal
    min: Decimal
    coin_price: Decimal

    class Config:
        from_attributes = True
