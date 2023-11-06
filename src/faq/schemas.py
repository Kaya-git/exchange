from pydantic import BaseModel


class FAQBase(BaseModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    ...

class FAQ(FAQBase):
    id: int

    class Config:
        orm_mode = True
