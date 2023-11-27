import asyncio
from decimal import Decimal

import redis.asyncio as redis
from fastapi import HTTPException, status
from sqlalchemy import update

from config import conf
from database.db import Database
from enums import CurrencyType, Status
from payment_options.models import PaymentOption
from pendings.models import PendingAdmin
from users.models import User

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
            (send_value - Decimal((send_value * margin) / 100) - gas) / coin_price
        )
        return get_value

    async def count_send_value(get_value, coin_price, margin, gas):
        send_value = (
            (coin_price + Decimal((get_value * margin) / 100) * get_value) + gas
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
        client_sell_tikker: str,
        client_buy_value: float,
        client_buy_tikker: str,
        client_credit_card_number: int,
        client_cc_holder: str,
        client_crypto_wallet: str,
        # client_sell_currency_po: str,
        # client_buy_currency_po: str
    ):
        await self.redis_conn.lpush(
            f"{user_uuid}",
            f"{client_email}",
            f"{client_sell_value}",
            f"{client_sell_tikker}",
            f"{client_buy_value}",
            f"{client_buy_tikker}",
            f"{client_credit_card_number}",
            f"{client_cc_holder}",
            f"{client_crypto_wallet}",
            # f"{client_sell_currency_po}",
            # f"{client_buy_currency_po}"
        )
        # await self.redis_conn.expire(name=f'{user_uuid}', time=900)
        self.redis_conn.close

    async def change_keys(self,
                          user_uuid,
                          order_id,
                          user_id
                          ):
        await self.redis_conn.delete(user_uuid)
        await self.redis_conn.lpush(
            user_uuid,
            order_id,
            user_id
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
            await services.redis_values.redis_conn.lindex(
                user_uuid,
                1
            )
        )
        order_id = int(order_id)
        """
        Делаем цикл с определенным количеством итераций для
        пулинга ордера из базы данных
        """
        while self.iterations != 0:
            order = None
            buy_po = None
            sell_po = None

            """
            Находим в бд заджойненый кортеж ордера со cпособами оплаты
            """
            order = await db.order.get(ident=order_id)
            buy_po = await db.payment_option.get_by_where(
                whereclause=(PaymentOption.id == order.buy_payment_option_id)
            )
            sell_po = await db.payment_option.get_by_where(
                whereclause=(PaymentOption.id == order.sell_payment_option_id)
            )
            if (
                order.status is Status.Verified and
                buy_po.is_verified is True and
                sell_po.is_verified is True
            ):
                await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                    )
                return "Верифицировали карту. Обмен разрешен"
                # return RedirectResponse(f"/exchange/order/{order.id}")
            if order.status is Status.NotVerified:
                await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                )
                await services.redis_values.redis_conn.delete(user_uuid)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"""Не удалось верифицировать карту:
                    {order.decline_reason}"""
                )
            await asyncio.sleep(30)
        await services.redis_values.redis_conn.delete(user_uuid)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="""Не удалось верифицировать карту,
                    истекло время"""
        )
        # return RedirectResponse("/cancel")

    async def payed_button_db(
        self,
        db: Database,
        user_uuid: str,
        order_id: int,
        user_id: int
    ):
        while self.iterations != 0:
            order = None
            order = await db.order.get(order_id)
            user = await db.user.get(user_id)
            if order.status is Status.Completed:
                await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                )

                buy_currency = await db.currency.get(order.buy_currency_id)
                sell_currency = await db.currency.get(order.sell_currency_id)
                if buy_currency.type is CurrencyType.Fiat:
                    user_volume = user.buy_volume
                    user_volume += order.user_buy_sum

                if sell_currency.type is CurrencyType.Fiat:
                    user_volume = user.buy_volume
                    user_volume += order.user_sell_sum

                statement = update(User).where(
                    User.id == user_id
                    ).values(buy_volume=user_volume)
                await db.session.execute(statement)
                await db.session.commit()
                await services.redis_values.redis_conn.delete(user_uuid)
                return " Успешно завершили обмен"
                # return RedirectResponse(f"exchange/succes/{order_id}")
            if order.status is Status.Canceled:
                await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                )
                await db.session.commit()
                await services.redis_values.redis_conn.delete(user_uuid)
                return "Не пришли средства, обмен отклонен"
                # return RedirectResponse(f"exchange/declined/{order_id}")
            await asyncio.sleep(30)


class Services:
    redis_values = RedisValues()
    db_paralell = DB(iterations=10)


services = Services()
