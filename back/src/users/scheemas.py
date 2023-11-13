from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from decimal import Decimal


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
