from fastapi import APIRouter, Form, UploadFile, Cookie, Depends
# from fastapi.responses import RedirectResponse
import os
from .sevices import Count
from .sevices import services
import secrets
from config import conf
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from bparser.parser import find_price
from database.models import (
    Currency, Status, CryptoType, User
)
from decimal import Decimal


forms_router = APIRouter(
    prefix="/forms",
    tags=["forms"]
)


# Форма для обмена
@forms_router.post("/exchange_form")
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

    """
    Проверяем пришли данные или нет
    """
    if (
        not client_sell_tikker_id or
        not client_buy_tikker_id or
        not client_email or
        not client_crypto_wallet or
        not client_credit_card_number or
        not client_cc_holder
    ):
        return KeyError

    client_sell_currency = await db.currency.get_by_where(
        Currency.tikker_id == client_sell_tikker_id
    )
    client_buy_currency = await db.currency.get_by_where(
        Currency.tikker_id == client_buy_tikker_id
    )

    """
    Разделяем пришедший тикер по '_'.
    Пример client_sell_currency_tikker и client_buy_currency_tikker:
        'RUB_SBER',
        'LTC_CRYPTO'
    """
    sell_currency_tuple = client_sell_currency.tikker.split("_")
    print(sell_currency_tuple)
    
    buy_currency_tuple = client_buy_currency.tikker.split("_")
    print(buy_currency_tuple)

    client_sell_currency_tikker = sell_currency_tuple[0]
    client_buy_currency_tikker = buy_currency_tuple[0]
    client_sell_currency_po = sell_currency_tuple[1]
    client_buy_currency_po = buy_currency_tuple[1]

    """
    Создаем строку для парсера равную условию: (Крипта)(Фиат)
    """
    if client_sell_currency.type != "Crypto":
        parser_tikker = (
            f"{client_buy_currency_tikker}{client_sell_currency_tikker}"
        )
    else:
        parser_tikker = (
            f"{client_sell_currency_tikker}{client_buy_currency_tikker}"
        )

    # -----
    """
    Забираем строку для определения коммиссии
    """
    margin = client_buy_currency.service_margin
    gas = client_buy_currency.gas
    """
    Просчитываем стоимость валюты с учетом коммисий и стоимости за перевод
    """
    coin_price = await find_price(parser_tikker)

    """
    Определяем какую строчку в форме заполнил пользователь и
    просчитываем стоимость
    """
    if client_sell_value != 0:
        try:
            client_buy_value = await Count.count_get_value(
                send_value=client_sell_value,
                coin_price=coin_price,
                margin=margin,
                gas=gas,
            )
        except KeyError("Ошибка в Client buy Value"):
            return ("Ошибка в Client buy Value")

    if client_sell_value == 0:
        try:
            client_sell_value = await Count.count_send_value(
                get_value=client_buy_value,
                coin_price=coin_price,
                margin=margin,
                gas=gas,
            )
        except KeyError("Ошибка в Client buy Value"):
            return ("Ошибка в Client buy Value")

    """
    Сохраняем переменные в редис под ключем = uuid пользователя
    """
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
            client_sell_currency_po=client_sell_currency_po,
            client_buy_currency_po=client_buy_currency_po
    )
    return "Redis - OK"
    # return RedirectResponse("/confirm")


# Форма для верификации карты по фото
@forms_router.post("/cc_conformation_form")
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

    """Проверяем формат картинки"""
    cc_image_name = cc_image.filename
    extension = cc_image_name.split(".")[1]
    print(extension)
    if extension not in ["png", "jpg", "JPG"]:
        return {"status": "error", "detail": "File extension is not allowed"}

    """Создаем новое название картинки,
    записываем в файл и отправляем на Яндекс диск"""
    new_file_name = f"{secrets.token_hex(10)}.{extension}"
    print(new_file_name)
    cc_image_content = await cc_image.read()

    with open(new_file_name, "wb") as file:
        file.write(cc_image_content)

    image_storage = await conf.image_storage.build_image_storage()

    await image_storage.upload(new_file_name, f"/exchange/{new_file_name}")
    await image_storage.close()
    os.remove(f"{new_file_name}")

    """ Достаем из редиса список с данными ордера."""
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

    """ Декодируем из бит в пайтоновские значения """
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

    client_sell_currency = await db.currency.get_by_where(
        Currency.tikker_id == client_sell_tikker_id
    )
    client_buy_currency = await db.currency.get_by_where(
        Currency.tikker_id == client_buy_tikker_id
    )

    """
    Проверяем существует ли ползователь с данным мылом,
    если нет создаем нового пользователя по email ордера с пустым паролем и
    возвращаем его из бд
    """

    user = await db.user.get_by_where(
        User.email == client_email
    )
    if user is None:
        new_user = await db.user.new(
            email=client_email,
        )
        db.session.add(new_user)
        await db.session.commit()
        user = await db.user.get_by_where(
            User.email == client_email
        )

    """
    Записываем расчетный способ в таблицу PaymentOption
    """
    if client_sell_currency.type == CryptoType.Fiat:

        client_sell_payment_option = await db.payment_option.new(
            banking_type=client_sell_currency_po,
            currency_id=client_sell_currency.id,
            number=client_credit_card_number,
            holder=client_cc_holder,
            image=new_file_name,
            user_id=user.id,
        )

        client_buy_payment_option = await db.payment_option.new(
            banking_type=client_buy_currency_po,
            currency_id=client_buy_currency.id,
            number=client_crypto_wallet,
            holder=client_email,
            user_id=user.id,
        )

        db.session.add_all(
            [client_sell_payment_option, client_buy_payment_option]
        )
        await db.session.flush()

    if client_sell_currency.type == CryptoType.Crypto:

        client_sell_payment_option = await db.payment_option.new(
            banking_type=client_buy_currency_po,
            currency_id=client_sell_currency.id,
            number=client_crypto_wallet,
            holder=client_email,
            user_id=user.id,
        )
        client_buy_payment_option = await db.payment_option.new(
            banking_type=client_sell_currency_po,
            currency_id=client_buy_currency.id,
            number=client_credit_card_number,
            holder=client_cc_holder,
            image=new_file_name,
            user_id=user.id,
        )

        db.session.add_all(
            [client_sell_payment_option, client_buy_payment_option]
        )
        await db.session.flush()

    """ Записываем новый ордер на обмен в базу данных """
    new_order = await db.order.new(
        user_id=user.id,
        user_email=client_email,
        user_cookie=user_uuid,
        user_buy_sum=client_buy_value,
        buy_currency_id=client_buy_currency.id,
        buy_payment_option_id=client_buy_payment_option.id,
        user_sell_sum=client_sell_value,
        sell_currency_id=client_sell_currency.id,
        sell_payment_option_id=client_sell_payment_option.id,
        status=Status.Pending,
    )

    db.session.add(new_order)
    await db.session.flush()

    """
    Заменить список с информацией в редисе на айди ордера
    """
    await services.redis_values.change_keys(
                    user_uuid=user_uuid,
                    order_id=new_order.id
                )

    await db.session.commit()

    return "Pending order created"
#         # return RedirectResponse("/exchange/await")
