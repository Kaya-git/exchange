from fastapi import APIRouter, HTTPException, status
from .schemas import UuidDTO
from config import conf
from sevices import services


where_am_i_router = APIRouter(
    prefix="/api/where_am_i",
    tags=["Роутер определения последней страницы пользователя"]
)


@where_am_i_router.post("/")
async def where_am_i(
    user_uuid: UuidDTO
):
    conf.log.logger.debug("Debug message")
    conf.log.logger.info("Info message")
    conf.log.logger.warning("Warning message")
    conf.log.logger.error("Error message")
    conf.log.logger.critical("Critical message")

    does_exist = await services.redis_values.redis_conn.exists(
        user_uuid.user_uuid
    )
    if does_exist != 1:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Пользователя нет в редисе"
        )
    router_number = (
            await services.redis_values.redis_conn.lindex(
                user_uuid.user_uuid,
                -1
            )
        )

    return router_number
