from typing import TYPE_CHECKING

from enums import BankingType
from pydantic import BaseModel

if TYPE_CHECKING:
    from currencies.schemas import CurrencyRead


class SPOAddDTO(BaseModel):
    banking_type: BankingType
    number: str
    holder: str
    currency_id: 'CurrencyRead'
    currency: 'CurrencyRead'


class SPODTO(SPOAddDTO):
    id: int

    class Config:
        from_attributes = True
