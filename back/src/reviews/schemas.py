from pydantic import BaseModel


class ReviewAddDTO(BaseModel):
    text: str
    rating: int
    name: str


class ReviewDTO(ReviewAddDTO):
    id: int

    class Config:
        from_attributes = True


class ReviewCreateDTO(BaseModel):
    name: str
    text: str | None
    rating: int
