import redis.asyncio as redis
from config import conf
from database.db import Database
from database.models import PendingOrder, Status
import asyncio
# from fastapi.responses import RedirectResponse


# Класс для пересчета операций с учетом маржи и комиссий
class Count:
    async def count_get_value(
        send_value,
        coin_price,
        margin, gas
    ):
        get_value = (
            (send_value - ((send_value * margin) / 100) - gas) / coin_price
        )
        return get_value

    async def count_send_value(get_value, coin_price, margin, gas):
        send_value = (
            (coin_price + ((get_value * margin) / 100) * get_value) + gas
        )
        return send_value


# Класс для работы с редис
class RedisValues:

    redis_conn = redis.Redis(host=conf.redis.host, port=conf.redis.port)

    async def set_order_info(
        self,
        user_id: str,
        client_email: str,
        client_send_value: float,
        send_tikker_id: int,
        client_get_value: float,
        get_tikker_id: str,
        client_cc_num: int,
        client_cc_holder_name: str,
        client_crypto_wallet: str
    ):
        await self.redis_conn.lpush(
            f"{user_id}",
            f"{client_email}",
            f"{client_send_value}",
            f"{send_tikker_id}",
            f"{client_get_value}",
            f"{get_tikker_id}",
            f"{client_cc_num}",
            f"{client_cc_holder_name}",
            f"{client_crypto_wallet}"
        )
        await self.redis_conn.expire(name=f'{user_id}', time=900)
        self.redis_conn.close

    async def change_keys(self,
                          user_id,
                          give_currency,
                          order_id,
                          ):
        await self.redis_conn.delete(user_id)
        await self.redis_conn.lpush(
            user_id,
            give_currency,
            order_id,
            )
        # await self.redis_conn.expire(
        #     name=f'{user_id}',
        #     time=1200
        # )
        self.redis_conn.close


class DB():

    def __init__(self, iterations):
        self.iterations = iterations

    async def conformation_await(self, db: Database, user_id: str):
        while self.iterations != 0:
            order = None
            try:
                order = await db.pending_order.get_by_where(
                    PendingOrder.user_uuid == user_id
                )
            except ValueError:
                return "Sosi Jopu"
            if order.status == Status.Approved:
                print(order.give_currency_id)
                await services.redis_values.change_keys(
                    user_id=user_id,
                    give_currency=order.give_currency_id,
                    order_id=order.id
                )
                print()
                return "Approved"
                # return RedirectResponse(f"/exchange/order/{order.id}")
            if order.status == Status.Canceled:
                # return RedirectResponse("/cancel")
                return "Order Canceled"
            await asyncio.sleep(30)

    async def payed_button_db(self, db: Database, user_id: str, order_id: int):
        while self.iterations != 0:
            pending_order = None
            pending_order = await db.pending_order.get_by_where(
                PendingOrder.id == order_id
            )
            print(f"pending_order: {pending_order.id},")
            if pending_order.status is Status.Completed:
                completed_order = await db.order.new(
                    email=pending_order.email,
                    give_amount=pending_order.give_amount,
                    give_currency_id=pending_order.give_currency_id,
                    get_amount=pending_order.get_amount,
                    get_currency_id=pending_order.get_currency_id,
                    status=pending_order.status,
                    # payment_options=pending_order.payment_options,
                    user_uuid=user_id,
                    # user_id=user_id
                )
                db.session.add(completed_order)
                print(f"completed_order_id: {completed_order.id}")
                await db.session.commit()
                # await db.pending_order.delete(PendingOrder.id == order_id)
                return "Заказ выполнен"
                # return RedirectResponse(f"exchange/succes/{order_id}")
            if pending_order.status is Status.Canceled:
                completed_order = await db.order.new(
                    email=pending_order.email,
                    give_amount=pending_order.give_amount,
                    give_currency_id=pending_order.give_currency_id,
                    get_amount=pending_order.get_amount,
                    get_currency_id=pending_order.get_currency_id,
                    # payment_options=pending_order.payment_options,
                    status=Status.Canceled,
                    user_uuid=user_id,
                    # user_id=user_id
                )
                db.session.add(completed_order)
                await db.session.commit()
                await db.pending_order.delete(PendingOrder.id == order_id)
                return "Оплата не проведена"
                # return RedirectResponse(f"exchange/declined/{order_id}")
            await asyncio.sleep(30)


class Services:
    redis_values = RedisValues()
    db_paralell = DB(iterations=10)


services = Services()
