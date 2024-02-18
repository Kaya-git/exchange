import asyncio
import json
from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import TYPE_CHECKING

import redis.asyncio as redis
from aiosmtplib import SMTP
from fastapi import HTTPException, status

from config import conf
from currencies.models import Currency
from database.db import Database
from enums import CurrencyType, Status
from payment_options.models import PaymentOption
from pendings.models import PendingAdmin
import logging


LOGGER = logging.getLogger(__name__)


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
            ) - gas) / Decimal(coin_price)
        )
        print(type(get_value))
        return get_value

    async def count_send_value(get_value, coin_price, margin, gas) -> Decimal:
        send_value = (
            (Decimal(coin_price) + Decimal(
                (get_value * margin) / 100
            ) * get_value) + gas
        )
        print(type(get_value))
        return send_value


class RedisValues:
    """Redis class"""
    redis_conn = redis.Redis(
        host=conf.redis.host,
        port=conf.redis.port,
        decode_responses=True
    )

    async def decirialize_b_to_dict(self) -> dict:
        b_data = await self.redis_conn.get("rates")

        return json.loads(b_data)

    # Достаем данные из редиса и декодируем их
    async def decode_values(
        self,
        user_uuid: str,
        db: Database,
        end_point_number: int = None
    ):
        if end_point_number == 4:
            (
                client_crypto_wallet,
                client_cc_holder,
                client_credit_card_number,
                client_buy_tikker,
                client_buy_value,
                client_sell_tikker,
                client_sell_value,
                client_email,
                router_number,
                order_id,
                user_id
            ) = await self.redis_conn.lrange(user_uuid, 0, -1)
        else:
            # Достаем из редиса список с данными ордера.
            (
                client_crypto_wallet,
                client_cc_holder,
                client_credit_card_number,
                client_buy_tikker,
                client_buy_value,
                client_sell_tikker,
                client_sell_value,
                client_email,
                router_number
            ) = await self.redis_conn.lrange(user_uuid, 0, -1)

        LOGGER.info(
            f"""
                Типы до десериализации:
                    client_crypto_wallet:{client_crypto_wallet} тип:{type(client_crypto_wallet)},
                    client_cc_holder:{client_cc_holder} тип:{type(client_cc_holder)},
                    client_credit_card_number:{client_credit_card_number} тип:{type(client_credit_card_number)},
                    client_buy_tikker:{client_buy_tikker} тип:{type(client_buy_tikker)},
                    client_buy_value:{client_buy_value} тип:{type(client_buy_value)},
                    client_sell_tikker:{client_sell_tikker} тип:{type(client_sell_tikker)},
                    client_sell_value:{client_sell_value} тип:{type(client_sell_value)},
                    client_email:{client_email} тип:{type(client_email)},
                    router_number:{router_number} тип:{type(router_number)}
            """
        )
        # Декодируем из бит в пайтоновские значения
        # client_sell_tikker = str(client_sell_tikker, 'UTF-8')
        client_sell_value = str(client_sell_value, 'UTF-8')
        client_credit_card_number = str(client_credit_card_number, 'UTF-8')
        client_cc_holder = str(client_cc_holder, 'UTF-8')

        client_crypto_wallet = str(client_crypto_wallet, 'UTF-8')
        client_buy_tikker = str(client_buy_tikker, 'UTF-8')
        client_buy_value = str(client_buy_value, 'UTF-8')

        client_email = str(client_email, 'UTF-8')

        router_number = int(router_number)

        client_sell_value = Decimal(client_sell_value)
        client_buy_value = Decimal(client_buy_value)

        client_sell_currency = await db.currency.get_by_where(
            Currency.tikker == client_sell_tikker
        )
        client_buy_currency = await db.currency.get_by_where(
            Currency.tikker == client_buy_tikker
        )

        LOGGER.info(
            f"""
                Типы после десериализации:
                    client_crypto_wallet:{client_crypto_wallet} тип:{type(client_crypto_wallet)},
                    client_cc_holder:{client_cc_holder} тип:{type(client_cc_holder)},
                    client_credit_card_number:{client_credit_card_number} тип:{type(client_credit_card_number)},
                    client_buy_tikker:{client_buy_tikker} тип:{type(client_buy_tikker)},
                    client_buy_value:{client_buy_value} тип:{type(client_buy_value)},
                    client_sell_tikker:{client_sell_tikker} тип:{type(client_sell_tikker)},
                    client_sell_value:{client_sell_value} тип:{type(client_sell_value)},
                    client_email:{client_email} тип:{type(client_email)},
                    router_number:{router_number} тип:{type(router_number)}
            """
        )
        return {
            "end_point_number": router_number,
            "client_email": client_email,
            "client_credit_card_number": client_credit_card_number,
            "client_cc_holder": client_cc_holder,
            "client_crypto_wallet": client_crypto_wallet,
            "client_sell_value": client_sell_value,
            "client_sell_currency": client_sell_currency.__dict__,
            "client_buy_value": client_buy_value,
            "client_buy_currency": client_buy_currency.__dict__,
        }

    async def set_ttl(
        self,
        user_uuid,
        time_out
    ):
        await self.redis_conn.expire(name=f'{user_uuid}', time=time_out)

    async def get_user_id(
            self,
            user_uuid: "UuidDTO"
    ) -> int | None:
        user_id = await self.redis_conn.lindex(
            user_uuid,
            10
        )

        if user_id is not None:
            return int(user_id)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отсутствует пользователь в редис"
        )

    async def get_order_id(
            self,
            user_uuid: str
    ) -> int | None:
        order_id = await self.redis_conn.lindex(
            user_uuid,
            9
        )
        if order_id is not None:
            return int(order_id)

        return None

    async def get_router_num(
            self,
            user_uuid: str
    ) -> int:
        router_num = await self.redis_conn.lindex(
            user_uuid,
            8
        )

        if router_num is not None:
            return int(router_num)
        return 0

    async def check_existance(
            self,
            user_uuid: str,
    ) -> bool | None:
        does_exist = await self.redis_conn.exists(
            user_uuid
        )

        if does_exist != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
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
            user_uuid,  # 0
            f"{end_point_number}",  # 8
            f"{client_email}",  # 7
            f"{client_sell_value}",  # 6
            f"{client_sell_tikker}",  # 5
            f"{client_buy_value}",  # 4
            f"{client_buy_tikker}",  # 3
            f"{client_credit_card_number}",  # 2
            f"{client_cc_holder}",  # 1
            f"{client_crypto_wallet}"  # 0
        )

        self.redis_conn.close

    async def add_keys(
        self,
        user_uuid: str,
        order_id: int,
        user_id: int,
    ):
        await self.redis_conn.rpush(
            user_uuid,
            order_id,  # 9
            user_id  # 10
            )
        self.redis_conn.close

    async def change_redis_router_num(
            self,
            user_uuid: str,
            router_num: int
    ):
        await self.redis_conn.lset(
            name=user_uuid,
            index=8,
            value=router_num
        )
        self.redis_conn.close


class DB:

    async def conformation_await(self, db: Database, user_uuid: str):
        """Забираем из редиса айди заказа"""

        # Получаем id ордера
        order_id = await services.redis_values.get_order_id(user_uuid)

        # Запускаем цикл который работает, пока сущствует ключ в редисе
        end_timer = await services.redis_values.redis_conn.ttl(name=user_uuid)
        while end_timer != -2:
            order = None
            buy_po = None
            sell_po = None

            # Получаем кортеж с заявкой из бд
            order = await db.order.get(ident=order_id)

            # Получаем кортеж со способом покупки из бд
            buy_po = await db.payment_option.get_by_where(
                whereclause=(PaymentOption.id == order.buy_payment_option_id)
            )

            # Получаем кортеж с валютой заказа из бд
            buy_currency = await db.currency.get(buy_po.currency_id)

            # Проверяем, если способ покупки Фиатный
            if buy_currency.type == CurrencyType.Фиат:

                # Проверяем, если карта прошла верификацию
                if buy_po.is_verified is True:

                    # Обновляем статус заявки
                    await db.order.order_status_update(
                        new_status=Status.ожидание_оплаты,
                        order_id=order_id
                    )
                    # Удаляем из актуальных заявок
                    await db.pending_admin.delete(
                        PendingAdmin.order_id == order_id
                    )
                    await db.session.commit()

                    # Выставляем таймер на время жизни заявки
                    await services.redis_values.set_ttl(
                        user_uuid=user_uuid,
                        time_out=600
                    )

                    return {
                        "verified": True
                    }

            # Получаем кортеж со способом продажи из бд
            sell_po = await db.payment_option.get_by_where(
                    whereclause=(
                        PaymentOption.id == order.sell_payment_option_id
                    )
                )

            # Проверяем, если способ покупки Фиатный
            if buy_currency.type != CurrencyType.Фиат:

                # Проверяем, если карта прошла верификацию
                if sell_po.is_verified is True:

                    await db.order.order_status_update(
                        new_status=Status.ожидание_оплаты,
                        order_id=order_id
                    )
                    await db.pending_admin.delete(
                        PendingAdmin.order_id == order_id
                    )
                    await db.session.commit()

                    # Выставляем таймер на время жизни заявки
                    await services.redis_values.set_ttl(
                        user_uuid=user_uuid,
                        time_out=120
                    )
                    return {
                        "verified": True
                    }
            # Если статус заявки отклонен
            if order.status is Status.отклонена:

                # Удаляем заявку из текущих
                await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                )
                await db.session.commit()

                # Удаляем ключ из редиса
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

        # Удаляем из текущих заявок
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
        # Запускаем цикл по оставшемуся времени заявки
        ttl = await services.redis_values.redis_conn.ttl(name=user_uuid)

        while ttl != -2:
            order = None
            order = await db.order.get(order_id)
            user = await db.user.get(user_id)

            # Проверяем что у заявки сменился статус на исполнена
            # И если заявка на приобретение криптовалюты,
            # То заполнено поле с сылкой на транзакцию

            if (
                order.status is Status.исполнена and
                order.transaction_link is not None
            ):

                buy_currency = await db.currency.get(order.buy_currency_id)

                # Проверяем валюту к приобретению
                if buy_currency.type is CurrencyType.Крипта:
                    user_volume = user.buy_volume
                    user_volume += order.user_sell_sum

                    # Обновляем обьем
                    await db.user.update_buy_volume(
                        ident=user_id,
                        user_volume=user_volume
                    )

                if buy_currency.type is CurrencyType.Фиат:
                    user_volume = user.buy_volume
                    user_volume += order.user_buy_sum

                    # Обновляем обьем
                    await db.user.update_sell_volume(
                        ident=user_id,
                        user_volume=user_volume
                    )
                # Удаляем заявки из акутальных и ключ в редисе
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

            # Если админ отклонил заявку
            if order.status is Status.отклонена:

                # Удаляем заявки из акутальных и ключ в редисе
                await db.pending_admin.delete(
                    PendingAdmin.order_id == order_id
                )
                await db.session.commit()
                await services.redis_values.redis_conn.delete(user_uuid)

                # Возращаем причину отказа
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
        message["Subject"] = "VVS COIN"
        message.attach(
            MIMEText(
                f"""
                <html><body><h1>Для подтверждения почты перейди по ссылке: \n
                https://dev.vvscoin.com/api/email_verif/verif?verif_token={
                    generated_token
                }<h1></body>
                """,
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
    db_paralell = DB()
    mail = Mail(
        email=conf.yandex_email,
        password=conf.yandex_email_pass
    )


services = Services()
