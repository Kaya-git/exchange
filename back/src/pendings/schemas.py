from enums.models import ReqAction
from pydantic import BaseModel


class PendingAdminAddDTO(BaseModel):
    req_act: ReqAction
    order_id: int
    review_id: int


class PendingAdminDTO(PendingAdminAddDTO):
    id: int

    class Config:
        from_attributes = True
