from pydantic import BaseModel


class UuidDTO(BaseModel):
    user_uuid: str
