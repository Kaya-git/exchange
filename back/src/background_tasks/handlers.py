from sevices import services
from asyncio import sleep as async_sleep
from redis_ttl.routers import get_ttl
from database.db import Database


async def controll_order(
    user_uuid: str | None,
    db: Database
):
    try:
        order_id = await services.redis_values.get_order_id(
            user_uuid=user_uuid
        )
        print(order_id)
    except:
        print("Нет ордера")

    order_ttl = await get_ttl(
        user_uuid=user_uuid
    )
    print(f"Запускаем цикл: {order_ttl}")
    while order_ttl != -2:
        if order_ttl == -1:
            print('У ключа не назначено время')
            return None
        print("Сплю 10 сек")
        await async_sleep(10)
        order_ttl = await get_ttl(
            user_uuid=user_uuid
        )
        print(order_ttl)
    print(f"Закончилось время: {order_ttl}")

    try:
        await db.order.order_status_timout(
            order_id
        )
    except:
        print("Заявки нет в бд")
    try:
        await db.pending_admin.delete(
            pending_admin.c.order_id == order_id
        )
        await db.session.commit()
    except:
        print("В пендинге нет заявки")
    return None
