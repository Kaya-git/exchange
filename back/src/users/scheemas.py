from pydantic import BaseModel


class ChangePassDTO(BaseModel):
    old_pass: str
    new_pass: str
