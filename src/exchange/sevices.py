import redis.asyncio as redis
from config import conf
from database.db import Database
from database.models import Order, Status
import asyncio
# from fastapi.responses import RedirectResponse


# Класс для пересчета операций с учетом маржи и комиссий
class Count:
    async def count_get_value(
        send_value,
        coin_price,
        margin,
        gas
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
        user_uuid: str,
        client_email: str,
        client_sell_value: float,
        client_sell_currency_tikker: str,
        client_buy_value: float,
        client_buy_currency_tikker: str,
        client_credit_card_number: int,
        client_cc_holder: str,
        client_crypto_wallet: str
    ):
        await self.redis_conn.lpush(
            f"{user_uuid}",
            f"{client_email}",
            f"{client_sell_value}",
            f"{client_sell_currency_tikker}",
            f"{client_buy_value}",
            f"{client_buy_currency_tikker}",
            f"{client_credit_card_number}",
            f"{client_cc_holder}",
            f"{client_crypto_wallet}"
        )
        # await self.redis_conn.expire(name=f'{user_uuid}', time=900)
        self.redis_conn.close

    async def change_keys(self,
                          user_uuid,
                          order_id,
                          ):
        await self.redis_conn.delete(user_uuid)
        await self.redis_conn.lpush(
            user_uuid,
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

    async def conformation_await(self, db: Database, user_uuid: str):
        while self.iterations != 0:
            order = None
            try:
                order = await db.order.get_by_where(
                    Order.user_cookie == user_uuid
                )
            except KeyError("Ошибка в conform_await"):
                return ("Ошибка в conform_await")
            if order.status == Status.Approved:
                print(order.sell_currency_tikker)
                await services.redis_values.change_keys(
                    user_uuid=user_uuid,
                    order_id=order.id
                )
                return "Approved"
                # return RedirectResponse(f"/exchange/order/{order.id}")
            if order.status == Status.Canceled:
                # return RedirectResponse("/cancel")
                return "Order Canceled"
            await asyncio.sleep(30)

    async def payed_button_db(
        self, db: Database,
        user_uuid: str, order_id: int
    ):
        while self.iterations != 0:
            order = None
            order = await db.order.get(order_id)
            print(f"pending_order: {order.id},")
            if order.status is Status.Completed:
                return "Заказ выполнен"
                # return RedirectResponse(f"exchange/succes/{order_id}")
            if order.status is Status.Canceled:
                return "Оплата не проведена"
                # return RedirectResponse(f"exchange/declined/{order_id}")
            await asyncio.sleep(30)


class Services:
    redis_values = RedisValues()
    db_paralell = DB(iterations=10)


services = Services()
