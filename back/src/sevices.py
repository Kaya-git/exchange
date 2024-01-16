import asyncio
from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import TYPE_CHECKING

import redis.asyncio as redis
from aiosmtplib import SMTP
from config import conf
from database.db import Database
from enums import CurrencyType, Status
from fastapi import HTTPException, status
from payment_options.models import PaymentOption
from pendings.models import PendingAdmin

if TYPE_CHECKING:
    from where_am_i.schemas import UuidDTO

Email = str
Pass = str
Token = str


# Класс для пересчета операций с учетом маржи и комиссий
class Count:
    async def count_get_value(
        send_value,
        coin_price,
        margin,
        gas
    ):
        get_value = (
            (send_value - Decimal(
                (send_value * margin) / 100
            ) - gas) / coin_price
        )
        return get_value

    async def count_send_value(get_value, coin_price, margin, gas):
        send_value = (
            (coin_price + Decimal(
                (get_value * margin) / 100
            ) * get_value) + gas
        )
        return send_value


class RedisValues:
    """Redis class"""
    redis_conn = redis.Redis(host=conf.redis.host, port=conf.redis.port)

    async def set_ttl(
        self,
        user_uuid,
        time_out
    ):
        await self.redis_conn.expire(name=f'{user_uuid}', time=time_out)

    async def get_user_id(
            self,
            user_uuid: "UuidDTO"
    ) -> int:
        user_id = await self.redis_conn.lindex(
            user_uuid,
            0
        )
        if user_id is None:
            return int(user_id)
        else:
            return None

    async def get_order_id(
            self,
            user_uuid: str
    ) -> int:
        order_id = await self.redis_conn.lindex(
            user_uuid,
            1
        )
        if order_id is not None:
            return int(order_id)
        else:
            return None

    async def get_router_num(
            self,
            user_uuid: str
    ) -> int:
        return await self.redis_conn.lindex(
            user_uuid,
            -1
        )

    async def check_existance(
            self,
            user_uuid: str,
            db: Database | None = None
    ) -> bool | None:
        does_exist = await self.redis_conn.exists(
            user_uuid
        )
        if does_exist != 1:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Пользователя нет в редисе"
            )
        else:
            return True

    async def set_order_info(
        self,
        user_uuid: str,
        end_point_number: int,
        client_email: str,
        client_sell_value: float,
        client_sell_tikker: str,
        client_buy_value: float,
        client_buy_tikker: str,
        client_credit_card_number: int,
        client_cc_holder: str,
        client_crypto_wallet: str,
    ):
        await self.redis_conn.lpush(
            f"{user_uuid}",
            f"{end_point_number}",
            f"{client_email}",
            f"{client_sell_value}",
            f"{client_sell_tikker}",
            f"{client_buy_value}",
            f"{client_buy_tikker}",
            f"{client_credit_card_number}",
            f"{client_cc_holder}",
            f"{client_crypto_wallet}"
        )

        # await self.set_ttl(user_uuid=user_uuid, time_out=120)
        # await self.redis_conn.expire(name=f'{user_uuid}', time=120)
        self.redis_conn.close

    async def change_keys(self,
                          user_uuid,
                          order_id,
                          user_id,
                          router_num
                          ):
        await self.redis_conn.delete(user_uuid)
        await self.redis_conn.lpush(
            user_uuid,
            router_num,
            order_id,
            user_id
            )
        await self.redis_conn.expire(
            name=f'{user_id}',
            time=10
        )
        self.redis_conn.close

    async def change_redis_router_num(
            self,
            user_uuid: str,
            router_num: int
    ):
        await self.redis_conn.lset(
            name=user_uuid,
            index=-1,
            value=router_num
        )
        self.redis_conn.close


class DB:

    def __init__(self, iterations):
        self.iterations = iterations

    async def conformation_await(self, db: Database, user_uuid: str):
        """
        Забираем из редиса айди заказа
        """
        await services.redis_values.check_existance(user_uuid)
        order_id = await services.redis_values.get_order_id(user_uuid)
        """
        Делаем цикл с определенным количеством итераций для
        пулинга ордера из базы данных
        """
        end_timer = await services.redis_values.redis_conn.ttl(name=user_uuid)

        while end_timer != 0:
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
            buy_currency = await db.currency.get(buy_po.currency_id)
            # Новая логика
            if buy_currency.type == CurrencyType.Фиат:
                if buy_po.is_verified is True:
                    await db.order.order_status_update(
                        new_status=Status.ожидание_оплаты,
                        order_id=order_id
                    )
                    await db.pending_admin.delete(
                        PendingAdmin.order_id == order_id
                    )
                    await db.session.commit()
                    return {
                        "verified": True
                    }

            sell_po = await db.payment_option.get_by_where(
                    whereclause=(
                        PaymentOption.id == order.sell_payment_option_id
                    )
                )
            if buy_currency.type != CurrencyType.Фиат:
                if sell_po.is_verified is True:
                    await db.order.order_status_update(
                        new_status=Status.ожидание_оплаты,
                        order_id=order_id
                    )
                    await db.pending_admin.delete(
                        PendingAdmin.order_id == order_id
                    )
                    await db.session.commit()
                    return {
                        "verified": True
                    }

            if order.status is Status.отклонена:
                await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                )
                await db.session.commit()
                await services.redis_values.redis_conn.delete(user_uuid)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"""Не удалось верифицировать карту:
                    {order.decline_reason}"""
                )
            await asyncio.sleep(5)
            end_timer = await services.redis_values.redis_conn.ttl(
                name=user_uuid
            )
        await services.redis_values.redis_conn.delete(user_uuid)
        await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                )
        await db.session.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="""Не удалось верифицировать карту,
                    истекло время"""
        )

    async def payed_button_db(
        self,
        db: Database,
        user_uuid: str,
        order_id: int,
        user_id: int
    ):
        ttl = await services.redis_values.redis_conn.ttl(name=user_uuid)

        while ttl != 0:
            order = None
            order = await db.order.get(order_id)
            user = await db.user.get(user_id)

            if (
                order.status is Status.исполнена and
                order.transaction_link is not None
            ):

                buy_currency = await db.currency.get(order.buy_currency_id)

                if buy_currency.type is CurrencyType.Крипта:
                    user_volume = user.buy_volume
                    user_volume += order.user_sell_sum

                    await db.user.update_buy_volume(
                        ident=user_id,
                        user_volume=user_volume
                    )

                if buy_currency.type is CurrencyType.Фиат:
                    user_volume = user.buy_volume
                    user_volume += order.user_buy_sum

                    await db.user.update_sell_volume(
                        ident=user_id,
                        user_volume=user_volume
                    )
                await services.redis_values.redis_conn.delete(user_uuid)
                await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                )
                await db.session.commit()
                if buy_currency.type is CurrencyType.Крипта:
                    return {
                        "link": order.transaction_link
                    }
                return None
            if order.status is Status.отклонена:
                await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                )
                await db.session.commit()
                await services.redis_values.redis_conn.delete(user_uuid)
                return {
                    "reason": order.decline_reason
                }
            await asyncio.sleep(5)


class Mail:

    def __init__(
            self,
            email: Email,
            password: Pass
    ) -> None:
        self.email = email
        self.password = password

    async def send_password(
            self,
            recepient_email: Email,
            generated_pass: Pass
    ) -> None:

        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = recepient_email
        message["Subject"] = "VSS COIN"
        message.attach(
            MIMEText(
                f"""<html><body><h1>Ваш пароль от лк VVS-Coin: \n
                {generated_pass}<h1></body>""",
                "html",
                "utf-8"
            )
        )

        smtp_client = SMTP(
            hostname='smtp.yandex.ru', port=465, use_tls=True, timeout=10
        )
        try:
            async with smtp_client:
                await smtp_client.login(self.email, self.password)
                await smtp_client.send_message(message)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Проблемы с отправлением сообщения на почту"
            )

    async def send_token(
            self,
            recepient_email: Email,
            generated_token: Token
    ):
        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = recepient_email
        message["Subject"] = "VSS COIN"
        message.attach(
            MIMEText(
                f"""<html><body><h1>Ваш токен для подтверждения VVS-Coin: \n
                {generated_token}<h1></body>""",
                "html",
                "utf-8"
            )
        )

        smtp_client = SMTP(
            hostname='smtp.yandex.ru', port=465, use_tls=True, timeout=10
        )
        try:
            async with smtp_client:
                await smtp_client.login(self.email, self.password)
                await smtp_client.send_message(message)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Проблемы с отправлением сообщения на почту"
            )


class Services:
    redis_values = RedisValues()
    db_paralell = DB(iterations=100)
    mail = Mail(
        email=conf.yandex_email,
        password=conf.yandex_email_pass
    )


services = Services()
