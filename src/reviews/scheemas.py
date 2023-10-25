from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class ReviewBase(BaseModel):
    text: str
    rating: Enum
    user_id: int

class ReviewCreation(ReviewBase):
    ...

class Review(ReviewBase):
    id: int
    data: datetime
