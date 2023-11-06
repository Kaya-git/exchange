from pydantic import BaseModel


class ContactBase(BaseModel):
    name: str
    link: str

class ContactCreate(ContactBase):
    ...


class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
