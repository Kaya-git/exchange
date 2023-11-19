from pydantic import BaseModel
from enums import BankingType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from currencies.schemas import CurrencyRead


class SPOBase(BaseModel):
    banking_type: BankingType
    number: str
    holder: str
    currency_id: 'CurrencyRead'
    currency: 'CurrencyRead'

class SPORead(SPOBase):
    id: int

    class Config:
        orm_mode = True

class SPOCreate(SPOBase):
    ...
