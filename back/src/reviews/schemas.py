from pydantic import BaseModel
from datetime import datetime


class ReviewAddDTO(BaseModel):
    text: str
    rating: int
    name: str
    date: datetime


class ReviewDTO(ReviewAddDTO):
    id: int

    class Config:
        from_attributes = True


class ReviewCreateDTO(BaseModel):
    name: str
    text: str | None
    rating: int
