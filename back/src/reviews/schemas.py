from pydantic import BaseModel


class ReviewAddDTO(BaseModel):
    text: str
    rating: int
    user_id: int
    moderated: bool


class ReviewDTO(ReviewAddDTO):
    id: int

    class Config:
        from_attributes = True


class ReviewCreateDTO(BaseModel):
    name: str
    text: str | None
    rating: int
