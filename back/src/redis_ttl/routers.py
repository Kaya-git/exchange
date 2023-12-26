from fastapi import APIRouter
from sevices import services


redis_router = APIRouter(
    prefix='api/redis/',
    tags=['Роутер редиса']
)


@redis_router.get('/ttl')
async def get_ttl(user_uuid: str | None) -> int:
    return await services.redis_values.redis_conn.ttl(name=user_uuid)
