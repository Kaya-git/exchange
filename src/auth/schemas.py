from fastapi_users import schemas
from typing import Optional
from database.models import Role


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    user_name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    registered_on: int
    role: Role


class UserCreate(schemas.BaseUserCreate):
    user_name: int
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    registered_on: int
    role: Role


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
