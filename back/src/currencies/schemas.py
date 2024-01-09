from decimal import Decimal
from typing import Optional

from enums import CurrencyType
from pydantic import BaseModel


class CurrencyAddDTO(BaseModel):
    coingecko_tik: str
    tikker: str
    type: CurrencyType
    name: str
    buy_gas: Decimal
    buy_margin: Decimal
    reserve: Decimal
    max: Decimal
    min: Decimal
    icon: Optional[str]


class CurrencyDTO(CurrencyAddDTO):
    id: int

    class Config:
        from_attributes = True


class CurrencyTariffsDTO(BaseModel):
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
