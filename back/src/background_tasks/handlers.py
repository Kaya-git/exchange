from sevices import services
from asyncio import sleep as async_sleep
from redis_ttl.routers import get_ttl
from database.db import Database


async def controll_order(
    user_uuid: str | None,
    db: Database
):
    router_num = await services.redis_values.get_router_num(
        user_uuid=user_uuid
    )

    # Получаем оставшееся время жизни ключа
    order_ttl = await get_ttl(
        user_uuid=user_uuid
    )
    print("Запускаем цикл")

    # Запускаем цикл, пока жив ключ
    while order_ttl != -2:

        # Если ключ -1 то не назначено время
        if order_ttl == -1:
            print('У ключа не назначено время')
            return None

        print("Сплю 10 сек")
        await async_sleep(10)

        order_ttl = await get_ttl(
            user_uuid=user_uuid
        )
        print(order_ttl)

    print("Закончилось время")

    # Если номер роутера больше 4, то создана заявка
    if router_num >= 3:
        order_id = await services.redis_values.get_order_id(
            user_uuid=user_uuid
        )
        print(order_id)

        # Меняем статус заявки на истекло время
        await db.order.order_status_timout(
            order_id
        )
        print("поменяли статус заявки")
    if (
        4 <= router_num >= 5 or
        7 <= router_num >= 8
    ):
        # Удаляем заявку из актуальных
        await db.pending_admin.delete(
            pending_admin.c.order_id == order_id
        )
        await db.session.commit()
        print("Удалили заявку в актуальных")
    else:
        print("Что то так")
        return
