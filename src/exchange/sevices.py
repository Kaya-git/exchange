import redis.asyncio as redis
from config import conf
from database.db import Database
from database.models import Order, Status, PaymentOption, BankingType
import asyncio
from sqlalchemy import select
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
        client_sell_tikker_id: int,
        client_buy_value: float,
        client_buy_tikker_id: int,
        client_credit_card_number: int,
        client_cc_holder: str,
        client_crypto_wallet: str,
        client_sell_currency_po: str,
        client_buy_currency_po: str
    ):
        await self.redis_conn.lpush(
            f"{user_uuid}",
            f"{client_email}",
            f"{client_sell_value}",
            f"{client_sell_tikker_id}",
            f"{client_buy_value}",
            f"{client_buy_tikker_id}",
            f"{client_credit_card_number}",
            f"{client_cc_holder}",
            f"{client_crypto_wallet}",
            f"{client_sell_currency_po}",
            f"{client_buy_currency_po}"
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
        """
        Забираем из редиса айди заказа
        """
        order_id = (
            await services.redis_values.redis_conn.lrange(
                user_uuid,
                0,
                -1,
            )
        )
        order_id = int(*order_id)
        """
        Делаем цикл с определенным количеством итераций для
        пулинга ордера из базы данных
        """
        while self.iterations != 0:
            order = None
            user_buy_po = None
            user_sell_po = None

            """
            Находим в бд заджойненый кортеж ордера со cпособами оплаты
            """
            order = await db.order.get(ident=order_id)

            statement = select(
                PaymentOption
                ).join(
                    Order, PaymentOption.id == Order.buy_payment_option_id
                    ).where(
                        Order.id == order_id
                    )
            user_buy_po = await db.session.execute(statement=statement)
            user_buy_po = user_buy_po.scalar_one_or_none()

            if user_buy_po.banking_type != BankingType.CRYPTO:
                if (
                    user_buy_po.is_verified is True and
                    order.status == Status.Approved
                ):
                    return "Верифицировали карту. Обмен разрешен"
                    # return RedirectResponse(f"/exchange/order/{order.id}")

            if user_buy_po.banking_type == BankingType.CRYPTO:
                statement = select(
                    PaymentOption
                ).join(
                    Order, PaymentOption.id == Order.sell_payment_option_id
                    ).where(
                        Order.id == order_id
                    )
                user_sell_po = await db.session.execute(statement=statement)
                user_sell_po = user_sell_po.scalar_one_or_none()
                if (
                    user_sell_po.is_verified is True and
                    order.status == Status.Approved
                ):
                    return "Верифицировали карту. Обмен разрешен"
                    # return RedirectResponse(f"/exchange/order/{order.id}")
            await asyncio.sleep(30)
        await services.redis_values.redis_conn.delete(user_uuid)
        return "Не удалось верифицировать карту"
        # return RedirectResponse("/cancel")

    async def payed_button_db(
        self,
        db: Database,
        user_uuid: str,
        order_id: int
    ):
        while self.iterations != 0:
            order = None
            order = await db.order.get(order_id)
            print(f"pending_order: {order.id},")
            if order.status is Status.Completed:
                await services.redis_values.redis_conn.delete(user_uuid)
                return " Успешно завершили обмен"
                # return RedirectResponse(f"exchange/succes/{order_id}")
            if order.status is Status.Canceled:
                await services.redis_values.redis_conn.delete(user_uuid)
                return "Не пришли средства, обмен отклонен"
                # return RedirectResponse(f"exchange/declined/{order_id}")
            await asyncio.sleep(30)


class Services:
    redis_values = RedisValues()
    db_paralell = DB(iterations=10)


services = Services()
