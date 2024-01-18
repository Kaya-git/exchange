from sevices import services
from asyncio import sleep as async_sleep
from redis_ttl.routers import get_ttl
from database.db import Database
from pendings.models import PendingAdmin
from enums.models import Status


async def controll_order(
    user_uuid: str | None,
    db: Database
):

    # Получаем оставшееся время жизни ключа
    order_ttl = await get_ttl(
        user_uuid=user_uuid
    )

    # Если ключ -1 то не назначено время
    if order_ttl == -1:
        return None

    # Запускаем цикл, пока жив ключ
    while order_ttl != -2:

        # Актуальный номер роутера
        router_num = await services.redis_values.get_router_num(
            user_uuid=user_uuid
        )

        # Если номер роутера от 3, то можно получить номер заявки
        if router_num >= 3:
            order_id = await services.redis_values.get_order_id(
                user_uuid=user_uuid
            )

        # Отдаем контроль на 10 сек
        await async_sleep(10)

        order_ttl = await get_ttl(
            user_uuid=user_uuid
        )

    # C 4 по 5 и с 7 по 8 заявка находиться актуальных
    if (
        4 <= router_num >= 5 or
        7 <= router_num >= 8
    ):
        # Удаляем заявку из актуальных
        await db.pending_admin.delete(
            PendingAdmin.order_id == order_id
        )
        await db.session.commit()

    if router_num >= 3:
        order = await db.order.get(order_id)
        if order.status != Status.исполнена:
            # Меняем статус заявки на истекло время
            await db.order.order_status_timout(
                order_id
            )
        return None
    else:
        return None
