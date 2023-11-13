from pydantic import BaseModel
from enums import Mark
from datetime import datetime


class ReviewBase(BaseModel):
    text: str
    data: datetime
    rating: Mark
    user_id: int

class ReviewCreation(ReviewBase):
    ...

class ReviewRead(ReviewBase):
    id: int
