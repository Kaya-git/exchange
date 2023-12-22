from fastapi import APIRouter
from .schemas import UuidDTO
from sevices import services


where_am_i_router = APIRouter(
    prefix="/api/where_am_i",
    tags=["Роутер определения последней страницы пользователя"]
)

RouterNumber = int


@where_am_i_router.post("/")
async def where_am_i(
    user_uuid: UuidDTO
) -> RouterNumber:
    if await services.redis_values.check_existance(user_uuid):
        return await services.redis_values.get_router_num(user_uuid)
