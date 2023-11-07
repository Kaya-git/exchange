from fastapi import APIRouter, Cookie, Depends, Form, UploadFile
from fastapi.responses import RedirectResponse
from sevices import services
from database.db import Database, get_async_session
from binance_parser import find_price
from currencies.models import Currency
from service_payment_options.models import ServicePaymentOption
from orders.models import Order
from enums import Status, CryptoType
from users.models import User
from payment_options.models import PaymentOption
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy import select, update
from pprint import pprint
from decimal import Decimal
from sevices import Count
import secrets
from config import conf
import os
from .handlers import (
    check_form_fillment,
    create_tikker_for_binance,
    check_if_values_empty,
    ya_save_passport_photo,
    redis_discard,
    add_or_get_po
)

exhange_router = APIRouter(
    prefix="/exchange",
    tags=["Роутер обмена"]
)


# Заполняем форму для обмена и передаем ее в редис
@exhange_router.post("/exchange_form")
async def order_crypto_fiat(
    client_sell_value: Decimal = Form(default=0),
    client_sell_tikker_id: int = Form(),
    client_buy_value: Decimal = Form(default=0),
    client_buy_tikker_id: int = Form(),
    client_email: str = Form(),
    client_crypto_wallet: str = Form(),
    client_credit_card_number: str = Form(),
    client_cc_holder: str = Form(),
    user_uuid: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session),
):
    db = Database(session=session)

    form_voc = {
       "client_sell_value": client_sell_value,
        "client_sell_tikker_id": client_sell_tikker_id,
        "client_buy_value": client_buy_value,
        "client_buy_tikker_id": client_buy_tikker_id,
        "client_email": client_email,
        "client_crypto_wallet": client_crypto_wallet,
        "client_credit_card_number": client_credit_card_number,
        "client_cc_holder": client_cc_holder,
        "user_uuid": user_uuid 
    }
    # Проверяем если все суммы равны нулю
    check = await check_if_values_empty(
        client_sell_value, client_buy_value
    )
    # Проверяем пришли данные или нет
    check = await check_form_fillment(form_voc)
    if check is not True:
        return check

    # Получем словарь с ссылкой для парсинга, типами оплаты и коммисиями
    parser_link_voc = await create_tikker_for_binance(
        db,
        client_sell_tikker_id,
        client_buy_tikker_id
    )
    # Просчитываем стоимость валюты с учетом коммисий и стоимости за перевод
    coin_price = await find_price(parser_link_voc["parser_tikker"])

    # Определяем какую строчку в форме заполнил пользователь и
    # просчитываем стоимость
    if client_sell_value != 0:
        try:
            client_buy_value = await Count.count_get_value(
                send_value=client_sell_value,
                coin_price=coin_price,
                margin=parser_link_voc["margin"],
                gas=parser_link_voc["gas"],
            )
        except KeyError("Ошибка в Client buy Value"):
            return ("Ошибка в Client buy Value")

    if client_sell_value == 0:
        try:
            client_sell_value = await Count.count_send_value(
                get_value=client_buy_value,
                coin_price=coin_price,
                margin=parser_link_voc["margin"],
                gas=parser_link_voc["gas"],
            )
        except KeyError("Ошибка в Client buy Value"):
            return ("Ошибка в Client buy Value")

    # Сохраняем переменные в редис под ключем = uuid пользователя
    await services.redis_values.set_order_info(
            user_uuid=user_uuid,
            client_email=client_email,
            client_sell_value=client_sell_value,
            client_sell_tikker_id=client_sell_tikker_id,
            client_buy_value=client_buy_value,
            client_buy_tikker_id=client_buy_tikker_id,
            client_credit_card_number=client_credit_card_number,
            client_cc_holder=client_cc_holder,
            client_crypto_wallet=client_crypto_wallet,
            client_sell_currency_po=parser_link_voc["client_sell_currency_po"],
            client_buy_currency_po=parser_link_voc["client_buy_currency_po"]
    )
    return "Redis - OK"
    # return RedirectResponse("/confirm")


@exhange_router.get("/confirm")
async def confirm_order(
    user_uuid: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    """
    Проверяем есть ли ключи в реддисе и забираем значения
    """
    does_exist = await services.redis_values.redis_conn.exists(user_uuid)
    if does_exist != 1:
        return "Время вышло"

    (
        client_buy_currency_po,
        client_sell_currency_po,
        client_crypto_wallet,
        client_cc_holder,
        client_credit_card_number,
        client_buy_tikker_id,
        client_buy_value,
        client_sell_tikker_id,
        client_sell_value,
        client_email
    ) = await services.redis_values.redis_conn.lrange(user_uuid, 0, -1)

    """
    Декодируем из бит в пайтоновские значения
    """
    client_sell_currency_po = str(client_sell_currency_po, 'UTF-8')
    client_sell_tikker_id = int(client_sell_tikker_id)
    client_sell_value = str(client_sell_value, 'UTF-8')
    client_credit_card_number = str(client_credit_card_number, 'UTF-8')
    client_cc_holder = str(client_cc_holder, 'UTF-8')

    client_buy_currency_po = str(client_buy_currency_po, 'UTF-8')
    client_crypto_wallet = str(client_crypto_wallet, 'UTF-8')
    client_buy_tikker_id = int(client_buy_tikker_id)
    client_buy_value = str(client_buy_value, 'UTF-8')

    client_email = str(client_email, 'UTF-8')

    client_sell_value = Decimal(client_sell_value)
    client_buy_value = Decimal(client_buy_value)

    """
    Проверяем зарегестрировани ли пользователь и
    верифицирована ли его банковская карта и

    """
    user = await db.user.get_by_where(
        User.email == client_email
    )
    if user is not None:
        credit_card = await db.payment_option.get_by_where(
            PaymentOption.number == client_credit_card_number
        )
        crypto_wallet = await db.payment_option.get_by_where(
            PaymentOption.number == client_crypto_wallet
        )
        client_sell_currency = await db.currency.get_by_where(
                Currency.tikker_id == client_sell_tikker_id
        )
        client_buy_currency = await db.currency.get_by_where(
                Currency.tikker_id == client_buy_tikker_id
        )
        if (
            crypto_wallet is not None and
            credit_card is not None and
            credit_card.is_verified is True
        ):
            if client_sell_currency.type == CryptoType.Fiat:
                new_order = await db.order.new(
                    user_id=user.id,
                    user_email=client_email,
                    user_cookie=user_uuid,
                    user_buy_sum=client_buy_value,
                    buy_currency_id=client_buy_currency.id,
                    buy_payment_option_id=crypto_wallet.id,
                    user_sell_sum=client_sell_value,
                    sell_currency_id=client_sell_currency.id,
                    sell_payment_option_id=credit_card.id,
                    status=Status.Pending,
                )
                db.session.add(new_order)
                await db.session.flush()
                await db.session.commit()
                await services.redis_values.change_keys(
                    user_uuid=user_uuid,
                    order_id=new_order.id
                )
            if client_sell_currency.type == CryptoType.Crypto:
                new_order = await db.order.new(
                    user_id=user.id,
                    user_email=client_email,
                    user_cookie=user_uuid,
                    user_buy_sum=client_buy_value,
                    buy_currency_id=client_buy_currency.id,
                    buy_payment_option_id=credit_card.id,
                    user_sell_sum=client_sell_value,
                    sell_currency_id=client_sell_currency.id,
                    sell_payment_option_id=crypto_wallet.id,
                    status=Status.Pending,
                )
                db.session.add(new_order)
                await db.session.flush()
                await db.session.commit()
                await services.redis_values.change_keys(
                    user_uuid=user_uuid,
                    order_id=new_order.id
                )
                return "Такой пользователь существует. Создан новый ордер"
        if (
            crypto_wallet is None and
            credit_card is not None and
            credit_card.is_verified is True
        ):
            if client_sell_currency.type == CryptoType.Fiat:
                crypto_wallet = await db.payment_option.new(
                    banking_type=client_buy_currency_po,
                    currency_id=client_buy_currency.id,
                    number=client_crypto_wallet,
                    holder=client_email,
                    user_id=user.id,
                )

                db.session.add(crypto_wallet)
                await db.session.flush()

                new_order = await db.order.new(
                    user_id=user.id,
                    user_email=client_email,
                    user_cookie=user_uuid,
                    user_buy_sum=client_buy_value,
                    buy_currency_id=client_buy_currency.id,
                    buy_payment_option_id=crypto_wallet.id,
                    user_sell_sum=client_sell_value,
                    sell_currency_id=client_sell_currency.id,
                    sell_payment_option_id=credit_card.id,
                    status=Status.Pending,
                )

                db.session.add(new_order)
                await db.session.flush()
                await db.session.commit()
                await services.redis_values.change_keys(
                    user_uuid=user_uuid,
                    order_id=new_order.id
                )
                return (
                    "Пользователь существует, банковская карта подтверждена,"
                    "криптовалютный кошель только зарегестрирован,"
                    "Создан новый ордер."
                )

            if client_sell_currency.type == CryptoType.Crypto:

                crypto_wallet = await db.payment_option.new(
                    banking_type=client_buy_currency_po,
                    currency_id=client_sell_currency.id,
                    number=client_crypto_wallet,
                    holder=client_email,
                    user_id=user.id,
                )

                db.session.add(crypto_wallet)
                await db.session.flush()

                new_order = await db.order.new(
                    user_id=user.id,
                    user_email=client_email,
                    user_cookie=user_uuid,
                    user_buy_sum=client_buy_value,
                    buy_currency_id=client_buy_currency.id,
                    buy_payment_option_id=credit_card.id,
                    user_sell_sum=client_sell_value,
                    sell_currency_id=client_sell_currency.id,
                    sell_payment_option_id=crypto_wallet.id,
                    status=Status.Pending,
                )

                db.session.add(new_order)
                await db.session.flush()
                await db.session.commit()
                await services.redis_values.change_keys(
                    user_uuid=user_uuid,
                    order_id=new_order.id
                )
                return (
                    "Пользователь существует, банковская карта подтверждена,"
                    "криптовалютный кошель только зарегестрирован,"
                    "Создан новый ордер."
                )

    # Возвращаем значения для подтверждения
    return {
        "client_sell_currency_po": client_sell_currency_po,
        "client_sell_tikker_id": client_sell_tikker_id,
        "client_sell_value": client_sell_value,
        "client_credit_card_number": client_credit_card_number,
        "client_cc_holder": client_cc_holder,
        "client_buy_currency_po": client_buy_currency_po,
        "client_crypto_wallet": client_crypto_wallet,
        "client_buy_tikker_id": client_buy_tikker_id,
        "client_buy_value": client_buy_value,
        "client_email": client_email
    }


# Отправляем фото паспорта на верификацию админу
@exhange_router.post("/cc_conformation_form")
async def confirm_cc(
    cc_image: UploadFile,
    user_uuid: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session)
):

    db = Database(session=session)

    """Проверяем есть ли ключи в реддисе"""
    does_exist = await services.redis_values.redis_conn.exists(user_uuid)
    if does_exist != 1:
        return "Время вышло"

    new_file_name = await ya_save_passport_photo(cc_image)

    redis_voc = await redis_discard(user_uuid, db)

    # Проверяем существует ли пользователь с данным мылом,
    # если нет создаем нового пользователя по email ордера с пустым паролем и
    # возвращаем его из бд
    user = await db.user.get_by_where(
        User.email == redis_voc["client_email"]
    )
    if user is None:
        new_user = await db.user.new(
            email=redis_voc["client_email"],
        )
        db.session.add(new_user)
        await db.session.commit()
        user = await db.user.get_by_where(
            User.email == redis_voc["client_email"]
        )

    p_o_dict = await add_or_get_po(
        db, redis_voc,
        user, new_file_name
    )

    # Записываем новый ордер на обмен в базу данных

    new_order = await db.order.new(
        user_id=user.id,
        user_email=redis_voc["client_email"],
        user_cookie=user_uuid,
        user_buy_sum=redis_voc["client_buy_value"],
        buy_currency_id=redis_voc["client_buy_currency"].id,
        buy_payment_option_id=p_o_dict["client_buy_payment_option"].id,
        user_sell_sum=redis_voc["client_sell_value"],
        sell_currency_id=redis_voc["client_sell_currency"].id,
        sell_payment_option_id=p_o_dict["client_sell_payment_option"].id,
        status=Status.Pending,
    )

    db.session.add(new_order)
    await db.session.flush()

    # Заменить список с информацией в редисе на айди ордера
    await services.redis_values.change_keys(
                    user_uuid=user_uuid,
                    order_id=new_order.id
                )

    await db.session.commit()

    return "Pending order created"
    # return RedirectResponse("/exchange/await")


@exhange_router.get("/await")
async def conformation_await(
    user_uuid: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session)
) -> RedirectResponse:

    db = Database(session=async_session)
    # Запускаем паралельно таск на пул из бд на подтверждение смены статуса ордера и верификации статуса пользователя
    paralel_waiting = asyncio.create_task(
        services.db_paralell.conformation_await(
            db,
            user_uuid
        )
    )
    answer = await paralel_waiting
    return answer


@exhange_router.get("/order")
async def requisites(
    async_session: AsyncSession = Depends(get_async_session),
    user_uuid: str | None = Cookie(default=None),
):
    db = Database(session=async_session)

    # Достаем из редиса тикер заказа
    order_id = (
        await services.redis_values.redis_conn.lrange(
            user_uuid,
            0,
            -1,
        )
    )
    order_id = int(*order_id)

    # Находим в таблице ServicePaymentOption способ оплаты
    # с тикером подходящим для продажи клиента
    statement = (
        select(
            ServicePaymentOption
            ).join(
            Currency, ServicePaymentOption.currency_id == Currency.id
            ).join(
                Order, Currency.id == Order.sell_currency_id
            ).where(
                Order.id == order_id
                )
    )

    service_payment_option = await db.session.execute(statement=statement)
    service_payment_option = service_payment_option.scalar_one_or_none()

    return {
            "requisites_num": service_payment_option.number,
            "holder": service_payment_option.holder
        }


@exhange_router.get("/payed",)
async def payed_button(
    async_session: AsyncSession = Depends(get_async_session),
    user_uuid: str | None = Cookie(default=None),
):
    db = Database(session=async_session)

    # Проверяем редис на наличие ключей,
    # если исчезли, то ставим статус ордера на просрок
    does_exist = await services.redis_values.redis_conn.exists(user_uuid)
    order_id = await services.redis_values.redis_conn.lindex(
        user_uuid,
        0
    )
    order_id = int(order_id)
    if not does_exist:
        statement = (
            update(Order).
            where(Order.id == order_id).
            values(status=Status.Timeout)
        )
        await db.session.execute(statement)
        return "Время вышло, по новой"

    task = asyncio.create_task(services.db_paralell.payed_button_db(
            db=db,
            user_uuid=user_uuid,
            order_id=order_id
        )
    )
    answer = await task
    return answer
