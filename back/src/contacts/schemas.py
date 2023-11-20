from pydantic import BaseModel


class ContactBase(BaseModel):
    name: str
    link: str

class ContactCreate(ContactBase):
    ...

class ContactRead(ContactBase):
    id: int

    class Config:
        from_attributes = True
