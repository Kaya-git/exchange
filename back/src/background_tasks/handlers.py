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
        print('У ключа не назначено время')
        return None

    print("Запускаем цикл")
    # Запускаем цикл, пока жив ключ
    while order_ttl != -2:

        # Актуальный номер роутера
        router_num = await services.redis_values.get_router_num(
            user_uuid=user_uuid
        )
        print(f"номер роутера: {router_num}")

        # Если номер роутера от 3, то можно получить номер заявки
        if router_num >= 3:
            order_id = await services.redis_values.get_order_id(
                user_uuid=user_uuid
            )
            print(f"номер заявки;{order_id}")

        # Отдаем контроль на 10 сек
        print("Сплю 10 сек")
        await async_sleep(10)

        order_ttl = await get_ttl(
            user_uuid=user_uuid
        )
        print(order_ttl)
    print("Закончилось время")

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
        print("Удалили заявку в актуальных")

    if router_num >= 3:
        order = await db.order.get(order_id)
        if order.status != Status.исполнена:
            # Меняем статус заявки на истекло время
            await db.order.order_status_timout(
                order_id
            )
            print("поменяли статус заявки")
        print("не меняли статус заявки")
        return None
    else:
        print("Заявка тайм аут раньше 3 роутера")
        return None
