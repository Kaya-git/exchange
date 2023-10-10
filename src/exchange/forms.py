from fastapi import APIRouter, Form, UploadFile, Cookie, Depends
# from fastapi.responses import RedirectResponse
import os
from .sevices import Count
from .sevices import services
import secrets
from config import conf
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from binance_parser import find_price
from .curency_dicts import CRYPTO_ID_TIKKERS, FIAT_ID_TIKKERS
from database.models import Currency, BankingType, Status, PaymentOption
from decimal import Decimal


forms_router = APIRouter(
    prefix="/forms",
    tags=["forms"]
)


# Форма для обмена
@forms_router.post("/exchange_form")
async def order_crypto_fiat(
    client_sell_value: Decimal = Form(default=0),
    client_sell_currency_tikker: str = Form(),
    client_buy_value: Decimal = Form(default=0),
    client_buy_currency_tikker: str = Form(),
    client_email: str = Form(),
    client_crypto_wallet: str = Form(),
    client_credit_card_number: str = Form(),
    client_cc_holder: str = Form(),
    user_uuid: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session),
):
    try:

        if client_sell_currency_tikker in CRYPTO_ID_TIKKERS:
            parser_tikker = (
                f"{client_sell_currency_tikker}{client_buy_currency_tikker}"
            )
        if client_sell_currency_tikker in FIAT_ID_TIKKERS:
            parser_tikker = (
                f"{client_buy_currency_tikker}{client_sell_currency_tikker}"
            )

    except KeyError("Тикера нет в словаре"):
        return ("Тикера нет в словаре")

    # -----

    db = Database(session=session)

    commissions = await db.currency.get_by_where(
        Currency.tikker == client_buy_currency_tikker
    )

    coin_price = await find_price(parser_tikker)

    if client_sell_value != 0:
        try:
            client_buy_value = await Count.count_get_value(
                send_value=client_sell_value,
                coin_price=coin_price,
                margin=commissions.service_margin,
                gas=commissions.gas,
            )
        except KeyError("Ошибка в Client buy Value"):
            return ("Ошибка в Client buy Value")

    if client_sell_value == 0:
        try:
            client_sell_value = await Count.count_send_value(
                get_value=client_buy_value,
                coin_price=coin_price,
                margin=commissions.service_margin,
                gas=commissions.gas,
            )
        except KeyError("Ошибка в Client buy Value"):
            return ("Ошибка в Client buy Value")

    try:
        await services.redis_values.set_order_info(
            user_uuid=user_uuid,
            client_email=client_email,
            client_sell_value=client_sell_value,
            client_sell_currency_tikker=client_sell_currency_tikker,
            client_buy_value=client_buy_value,
            client_buy_currency_tikker=client_buy_currency_tikker,
            client_credit_card_number=client_credit_card_number,
            client_cc_holder=client_cc_holder,
            client_crypto_wallet=client_crypto_wallet,
        )
    except KeyError("Ошибка в Редис"):
        return ("Ошибка в Редис")
    return "Redis - OK"
    # return RedirectResponse("/confirm")


# Форма для верификации карты по фото
@forms_router.post("/cc_conformation_form")
async def confirm_cc(
    cc_image: UploadFile,
    user_uuid: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session)
):

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
        client_crypto_wallet,
        client_cc_holder,
        client_credit_card_number,
        client_buy_currency_tikker,
        client_buy_value,
        client_sell_currency_tikker,
        client_sell_value,
        client_email
    ) = await services.redis_values.redis_conn.lrange(user_uuid, 0, -1)

    client_crypto_wallet = str(client_crypto_wallet, 'UTF-8')
    client_cc_holder = str(client_cc_holder, 'UTF-8')
    client_credit_card_number = str(client_credit_card_number, 'UTF-8')
    client_buy_currency_tikker = str(client_buy_currency_tikker, 'UTF-8')
    client_buy_value = str(client_buy_value, 'UTF-8')
    client_sell_currency_tikker = str(client_sell_currency_tikker, 'UTF-8')
    client_sell_value = str(client_sell_value, 'UTF-8')
    client_email = str(client_email, 'UTF-8')
    client_buy_value = Decimal(client_buy_value)
    client_sell_value = Decimal(client_sell_value)

    db = Database(session=session)

    """ Записываем расчетный способ в таблицу PaymentOption """
    if client_sell_currency_tikker in FIAT_ID_TIKKERS:

        client_sell_payment_option = await db.payment_option.new(
            banking_type=BankingType.BankingCard,
            currency_tikker=client_sell_currency_tikker,
            number=client_credit_card_number,
            holder=client_cc_holder,
            image=new_file_name,
            user_email=client_email,
        )

        client_buy_payment_option = await db.payment_option.new(
            banking_type=BankingType.CryptoWallet,
            currency_tikker=client_buy_currency_tikker,
            number=client_crypto_wallet,
            holder=client_email,
            user_email=client_email,
        )

        db.session.add_all(
            [client_sell_payment_option, client_buy_payment_option]
        )
        await db.session.commit()
        client_sell_payment_option = await db.payment_option.get_by_where(
            PaymentOption.number == client_credit_card_number
        )
        client_buy_payment_option = await db.payment_option.get_by_where(
            PaymentOption.number == client_crypto_wallet
        )

    if client_sell_currency_tikker in CRYPTO_ID_TIKKERS:

        client_sell_payment_option = await db.payment_option.new(
            banking_type=BankingType.CryptoWallet,
            currency_tikker=client_buy_currency_tikker,
            number=client_crypto_wallet,
            holder=client_email,
            user_email=client_email,
        )
        client_buy_payment_option = await db.payment_option.new(
            banking_type=BankingType.BankingCard,
            currency_tikker=client_sell_currency_tikker,
            number=client_credit_card_number,
            holder=client_cc_holder,
            image=new_file_name,
            user_email=client_email,
        )

        db.session.add_all(
            [client_sell_payment_option, client_buy_payment_option]
        )
        await db.session.commit()
        client_sell_payment_option = await db.payment_option.get_by_where(
            PaymentOption.number == client_crypto_wallet
        )
        client_buy_payment_option = await db.payment_option.get_by_where(
            PaymentOption.number == client_credit_card_number
        )

    """ Записываем новый ордер на обмен в базу данных """
    new_order = await db.order.new(
        user_email=client_email,
        user_cookie=user_uuid,
        user_buy_sum=client_buy_value,
        buy_currency_tikker=client_buy_currency_tikker,
        buy_payment_option=client_buy_payment_option.id,
        user_sell_sum=client_sell_value,
        sell_currency_tikker=client_sell_currency_tikker,
        sell_payment_option=client_sell_payment_option.id,
        status=Status.Pending,
    )
    db.session.add(new_order)
    await db.session.commit()
    return "Pending order created"
#         # return RedirectResponse("/exchange/await")
