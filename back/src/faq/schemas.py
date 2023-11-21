from pydantic import BaseModel


class FAQBase(BaseModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    ...

class FAQRead(FAQBase):
    id: int

    class Config:
        from_attributes = True
