from datetime import datetime
from pydantic import BaseModel

from enums import Mark


class ReviewAddDTO(BaseModel):
    text: str
    data: datetime
    rating: Mark
    user_id: int


class ReviewDTO(ReviewAddDTO):
    id: int

    class Config:
        from_attributes = True


class ReviewCreateDTO(BaseModel):
    text: str | None
    rating: Mark
