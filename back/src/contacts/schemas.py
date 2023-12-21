from pydantic import BaseModel


class ContactAddDTO(BaseModel):
    name: str
    link: str


class ContactDTO(ContactAddDTO):
    id: int

    class Config:
        from_attributes = True
