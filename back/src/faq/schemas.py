from pydantic import BaseModel


class FAQAddDTO(BaseModel):
    question: str
    answer: str


class FAQDTO(FAQAddDTO):
    id: int

    class Config:
        from_attributes = True
