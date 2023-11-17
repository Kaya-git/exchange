from typing import Optional
from database.db import Database
from currencies.models import Currency
from enums import CurrencyType
from payment_options.models import PaymentOption
import secrets
import os
from config import conf
from sevices import services
from decimal import Decimal
from users.models import User
from fastapi import status, HTTPException
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def generate_pass():
    return secrets.token_hex(10)

async def send_email(
    recepient_email,
    generated_pass
):
    email = conf.yandex_email
    password = conf.yandex_email_pass

    msg = MIMEText(f"Ваш пароль от лк VVS-Coin: {generated_pass}", 'plain', 'utf-8')
    msg['Subject'] = Header('Пароль от лк VVS-Coin', 'utf-8')
    msg['From'] = email
    msg['To'] = recepient_email

    s = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)

    try:
        s.starttls()
        s.login(email, password)
        s.sendmail(msg['From'], recepient_email, msg.as_string())
    except Exception as ex:
        print(ex)
    finally:
        s.quit()
    return generated_pass


async def check_form_fillment(
        form_voc
) -> None:
    if not form_voc["client_sell_value"] and not form_voc["client_buy_value"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не указал ни одну сумму для обмена"
        )
    if form_voc["client_sell_value"] == 0 and form_voc["client_buy_value"] == 0:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Клиент указал нули на суммах для перевода"
        )
    if not form_voc["client_sell_tikker_id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не указал айди тиккера продажи"
        )
    if not form_voc["client_buy_tikker_id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не указал айди тиккера покупки"
        )
    if not form_voc["client_email"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не указал почту"
        )
    if not form_voc["client_crypto_wallet"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не указал крипто кошелек"
        )
    if not form_voc["client_credit_card_number"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не указал номер карты"
        )
    if not form_voc["client_cc_holder"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не указал владельца кредитной карты"
        )
    if not form_voc["user_uuid"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У клиента нет куки с айди"
        )


# Разделяем пришедший тикер по '_'.
# Пример client_sell_currency_tikker и client_buy_currency_tikker:
#   'RUB_SBER',
#   'LTC_CRYPTO'
async def create_tikker_for_binance(
        db: Database,
        client_sell_tikker_id,
        client_buy_tikker_id
) -> dict:

    client_sell_currency = await db.currency.get_by_where(
        Currency.tikker_id == client_sell_tikker_id
    )
    client_buy_currency = await db.currency.get_by_where(
        Currency.tikker_id == client_buy_tikker_id
    )
    if not client_sell_currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="В базе данных нет такого номера тикера на продажи"
        )
    if not client_buy_tikker_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="В базе данных нет такого номера тикера на покупку"
        )

    sell_currency_tuple = client_sell_currency.tikker.split("_")
    buy_currency_tuple = client_buy_currency.tikker.split("_")

    client_sell_currency_tikker = sell_currency_tuple[0]
    client_buy_currency_tikker = buy_currency_tuple[0]
    client_sell_currency_po = sell_currency_tuple[1]
    client_buy_currency_po = buy_currency_tuple[1]

    # Создаем строку для парсера равную условию: (Крипта)(Фиат) 
    if client_sell_currency.type == CurrencyType.Crypto:
        parser_tikker = (
            f"{client_sell_currency_tikker}{client_buy_currency_tikker}"
        )
        margin = 0
        gas = 0

    if client_sell_currency.type == CurrencyType.Fiat:
        parser_tikker = (
            f"{client_buy_currency_tikker}{client_sell_currency_tikker}"
        )
        margin = client_buy_currency.service_margin
        gas = client_buy_currency.gas

    return {
            "parser_tikker": parser_tikker,
            "client_sell_currency": client_sell_currency,
            "client_buy_currency": client_buy_currency,
            "client_sell_currency_po": client_sell_currency_po,
            "client_buy_currency_po": client_buy_currency_po,
            "margin": margin,
            "gas": gas
        }


# Сохраняем картинку
async def ya_save_passport_photo(
        cc_image
):
    try:
        # Проверяем формат картинки
        cc_image_name = cc_image.filename
        extension = cc_image_name.split(".")[1]
        print(extension)
        if extension not in ["png", "jpg", "JPG"]:
            return {"status": "error", "detail": "File extension is not allowed"}

        # Создаем новое название картинки,
        # записываем в файл и отправляем на Яндекс диск
        new_file_name = f"{secrets.token_hex(10)}.{extension}"
        cc_image_content = await cc_image.read()

        with open(new_file_name, "wb") as file:
            file.write(cc_image_content)

        image_storage = await conf.image_storage.build_image_storage()

        await image_storage.upload(new_file_name, f"/exchange/{new_file_name}")
        await image_storage.close()
        os.remove(f"{new_file_name}")
        return new_file_name
    except Exception as ex:
        return ex


# Достаем данные из редиса и декодируем их
async def redis_discard(
        user_uuid: str | None,
        db: Database
):
    # Достаем из редиса список с данными ордера.
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

    # Декодируем из бит в пайтоновские значения
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
        "client_email": client_email,
        "client_sell_currency": client_sell_currency,
        "client_buy_currency": client_buy_currency
    }


async def add_or_get_po(
        db: Database,
        redis_voc: dict,
        user: User,
        new_file_name: str
):
    crypto_po = await db.payment_option.get_by_where(
        PaymentOption.number == redis_voc["client_crypto_wallet"]
    )
    fiat_po = await db.payment_option.get_by_where(
        PaymentOption.number == redis_voc["client_credit_card_number"]
    )
    # client_sell_currency = redis_voc["client_sell_currency"]
    # client_buy_currency = redis_voc["client_buy_currency"]
    # print(crypto_po.id)
    # print(fiat_po.id)
    if crypto_po is None and fiat_po is None:

        if redis_voc["client_sell_currency"].type == CurrencyType.Fiat:

            client_sell_payment_option = await db.payment_option.new(
                banking_type=redis_voc["client_sell_currency_po"],
                currency_id=redis_voc["client_sell_currency"].id,
                number=redis_voc["client_credit_card_number"],
                holder=redis_voc["client_cc_holder"],
                image=new_file_name,
                user_id=user.id,
            )

            client_buy_payment_option = await db.payment_option.new(
                banking_type=redis_voc["client_buy_currency_po"],
                currency_id=redis_voc["client_buy_currency"].id,
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user.id,
            )

        if redis_voc["client_sell_currency"].type == CurrencyType.Crypto:

            client_sell_payment_option = await db.payment_option.new(
                banking_type=redis_voc["client_buy_currency_po"],
                currency_id=redis_voc["client_sell_currency"].id,
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user.id,
            )
            client_buy_payment_option = await db.payment_option.new(
                banking_type=redis_voc["client_sell_currency_po"],
                currency_id=redis_voc["client_buy_currency"].id,
                number=redis_voc["client_credit_card_number"],
                holder=redis_voc["client_cc_holder"],
                image=new_file_name,
                user_id=user.id,
            )

        db.session.add_all(
            [client_sell_payment_option, client_buy_payment_option]
        )

    if (
        crypto_po is not None and
        # crypto_po.user_id == user.email and
        fiat_po is None
    ):
        print("yes1")
        if redis_voc["client_sell_currency"].type == CurrencyType.Fiat:

            client_sell_payment_option = await db.payment_option.new(
                banking_type=redis_voc["client_sell_currency_po"],
                currency_id=redis_voc["client_sell_currency"].id,
                number=redis_voc["client_credit_card_number"],
                holder=redis_voc["client_cc_holder"],
                image=new_file_name,
                user_id=user.id,
            )

            client_buy_payment_option = crypto_po

            db.session.add(client_sell_payment_option)

        if redis_voc["client_sell_currency"].type == CurrencyType.Crypto:

            client_sell_payment_option = crypto_po

            client_buy_payment_option = await db.payment_option.new(
                banking_type=redis_voc["client_sell_currency_po"],
                currency_id=redis_voc["client_buy_currency"].id,
                number=redis_voc["client_credit_card_number"],
                holder=redis_voc["client_cc_holder"],
                image=new_file_name,
                user_id=user.id,
            )

            db.session.add(client_buy_payment_option)

    if (
        fiat_po is not None and
        str(fiat_po.user_id) == user.email and
        crypto_po is None
    ):
        print("yes2")
        if redis_voc["client_sell_currency"].type == CurrencyType.Fiat:

            client_sell_payment_option = fiat_po

            client_buy_payment_option = await db.payment_option.new(
                banking_type=redis_voc["client_buy_currency_po"],
                currency_id=redis_voc["client_buy_currency"].id,
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user.id,
            )
            db.session.add(client_buy_payment_option)

        if redis_voc["client_sell_currency"].type == CurrencyType.Crypto:

            client_sell_payment_option = await db.payment_option.new(
                banking_type=redis_voc["client_buy_currency_po"],
                currency_id=redis_voc["client_sell_currency"].id,
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user.id,
            )
            client_buy_payment_option = fiat_po
            db.session.add(client_sell_payment_option)

    if (
        fiat_po is not None and 
        crypto_po is not None
    ):
        print("yes3")
        if str(fiat_po.user) != user.email:
            
            print(f"{fiat_po.user}{type(fiat_po.user)}")
            print(f"{user.email}{type(user.email)}")
            return {"Номер карты зарегестрирован под другим имейлом"}
        if str(crypto_po.user) != user.email:
            return {"Крипто Кошель зарегестрирован под другим имейлом"}
        client_sell_payment_option = fiat_po
        client_buy_payment_option = fiat_po
    await db.session.flush()
    return {
            "client_sell_payment_option": client_sell_payment_option,
            "client_buy_payment_option": client_buy_payment_option
        }
