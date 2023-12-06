import os
import secrets
import smtplib
from decimal import Decimal
from email.header import Header
from email.mime.text import MIMEText

from fastapi import HTTPException, status
from passlib.context import CryptContext

from binance_parser import find_price
from config import conf
from currencies.models import Currency
from database.db import Database
from enums import CurrencyType, Status
from payment_options.models import PaymentOption
from sevices import Count, services
from users.models import User


async def get_password_hash(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


async def generate_pass():
    return secrets.token_hex(10)


async def send_email(
    recepient_email,
    generated_pass
):
    email = conf.yandex_email
    password = conf.yandex_email_pass

    msg = MIMEText(
        f"Ваш пароль от лк VVS-Coin: {generated_pass}",
        'plain', 'utf-8'
    )
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
    if (form_voc["client_sell_value"] == 0 and
            form_voc["client_buy_value"] == 0):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Клиент указал нули на суммах для перевода"
        )
    if form_voc["client_sell_tikker"] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не указал айди тиккера продажи"
        )
    if form_voc["client_buy_tikker"] is None:
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
    return True


# Сохраняем картинку
async def ya_save_passport_photo(
        cc_image
):
    try:
        # Проверяем формат картинки
        cc_image_name = cc_image.filename
        extension = cc_image_name.split(".")[1]

        # if extension not in ["png", "jpg", "JPG"]:
        #     return {
        #         "status": "error",
        #         "detail": "File extension is not allowed"
        #     }

        # Создаем новое название картинки,
        # записываем в файл и отправляем на Яндекс диск
        new_file_name = f"{secrets.token_hex(10)}.{extension}"
        cc_image_content = await cc_image.read()

        with open(new_file_name, "wb") as file:
            file.write(cc_image_content)

        image_storage = await conf.image_storage.build_image_storage()

        await image_storage.upload(new_file_name, f"/exchange/{new_file_name}")
        await image_storage.close()
        # os.remove(f"{new_file_name}")
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
        client_crypto_wallet,
        client_cc_holder,
        client_credit_card_number,
        client_buy_tikker,
        client_buy_value,
        client_sell_tikker,
        client_sell_value,
        client_email
    ) = await services.redis_values.redis_conn.lrange(user_uuid, 0, -1)

    # Декодируем из бит в пайтоновские значения
    client_sell_tikker = str(client_sell_tikker, 'UTF-8')
    client_sell_value = str(client_sell_value, 'UTF-8')
    client_credit_card_number = str(client_credit_card_number, 'UTF-8')
    client_cc_holder = str(client_cc_holder, 'UTF-8')

    # client_buy_currency_po = str(client_buy_currency_po, 'UTF-8')
    client_crypto_wallet = str(client_crypto_wallet, 'UTF-8')
    client_buy_tikker = str(client_buy_tikker, 'UTF-8')
    client_buy_value = str(client_buy_value, 'UTF-8')

    client_email = str(client_email, 'UTF-8')

    client_sell_value = Decimal(client_sell_value)
    client_buy_value = Decimal(client_buy_value)

    client_sell_currency = await db.currency.get_by_where(
        Currency.tikker == client_sell_tikker
    )
    client_buy_currency = await db.currency.get_by_where(
        Currency.tikker == client_buy_tikker
    )

    return {
        "client_email": client_email,
        "client_credit_card_number": client_credit_card_number,
        "client_cc_holder": client_cc_holder,
        "client_crypto_wallet": client_crypto_wallet,
        "client_sell_value": client_sell_value,
        "client_sell_currency": client_sell_currency,
        "client_buy_value": client_buy_value,
        "client_buy_currency": client_buy_currency,
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

    if crypto_po is None and fiat_po is None:

        if redis_voc["client_sell_currency"].type == CurrencyType.Fiat:

            client_sell_payment_option = await db.payment_option.new(
                # banking_type=redis_voc["client_sell_currency"]["tikker"],
                currency_id=redis_voc["client_sell_currency"].id,
                number=redis_voc["client_credit_card_number"],
                holder=redis_voc["client_cc_holder"],
                image=new_file_name,
                user_id=user.id,
            )

            client_buy_payment_option = await db.payment_option.new(
                # banking_type=redis_voc["client_buy_currency"]["tikker"],
                currency_id=redis_voc["client_buy_currency"].id,
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user.id,
            )

        if redis_voc["client_sell_currency"].type == CurrencyType.Crypto:

            client_sell_payment_option = await db.payment_option.new(
                # banking_type=redis_voc["client_buy_currency_po"],
                currency_id=redis_voc["client_sell_currency"].id,
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user.id,
            )
            client_buy_payment_option = await db.payment_option.new(
                # banking_type=redis_voc["client_sell_currency_po"],
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
                # banking_type=redis_voc["client_sell_currency_po"],
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
                # banking_type=redis_voc["client_sell_currency_po"],
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

        if redis_voc["client_sell_currency"].type == CurrencyType.Fiat:

            client_sell_payment_option = fiat_po

            client_buy_payment_option = await db.payment_option.new(
                # banking_type=redis_voc["client_buy_currency_po"],
                currency_id=redis_voc["client_buy_currency"].id,
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user.id,
            )
            db.session.add(client_buy_payment_option)

        if redis_voc["client_sell_currency"].type == CurrencyType.Crypto:

            client_sell_payment_option = await db.payment_option.new(
                # banking_type=redis_voc["client_buy_currency_po"],
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
        if str(fiat_po.user) != user.email:
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


async def calculate_totals(
        client_sell_coin,
        client_buy_coin,
        coin_price,
        client_sell_value,
        client_buy_value
):
    if client_sell_value != 0:

        if client_sell_coin.type == CurrencyType.Crypto:

            client_buy_value = round(await Count.count_send_value(
                get_value=client_sell_value,
                coin_price=coin_price,
                margin=client_buy_coin.buy_margin,
                gas=client_buy_coin.buy_gas,
            ), 2)
            if client_buy_value is None:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Клиент указал ноль на покупке"
                )
        if client_sell_coin.type == CurrencyType.Fiat:

            client_buy_value = round(await Count.count_get_value(
                send_value=client_sell_value,
                coin_price=coin_price,
                margin=client_buy_coin.buy_margin,
                gas=client_buy_coin.buy_gas,
            ), 4)
            if client_buy_value is None:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Клиент указал ноль на покупке"
                )

    if client_sell_value == 0:

        if client_buy_coin.type == CurrencyType.Crypto:

            client_sell_value = round(await Count.count_send_value(
                get_value=client_buy_value,
                coin_price=coin_price,
                margin=client_buy_coin.buy_margin,
                gas=client_buy_coin.buy_gas,
            ), 2)
            if client_sell_value is None:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Клиент указал ноль на продаже"
                )
        if client_buy_coin.type == CurrencyType.Fiat:

            client_sell_value = round(await Count.count_get_value(
                send_value=client_buy_value,
                coin_price=coin_price,
                margin=client_buy_coin.buy_margin,
                gas=client_buy_coin.buy_gas,
            ), 4)
            if client_sell_value is None:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Клиент указал ноль на продаже"
                )
    return {
        "client_sell_value": client_sell_value,
        "client_buy_value": client_buy_value
    }


async def find_exchange_rate(
    client_sell_coin,
    client_buy_coin
):

    if client_sell_coin.coingecko_tik == "rub":
        ids = client_buy_coin.coingecko_tik
        vs_currencies = client_sell_coin.coingecko_tik

    if client_buy_coin.coingecko_tik == "rub":
        ids = client_sell_coin.coingecko_tik
        vs_currencies = client_buy_coin.coingecko_tik

    coin_price = await find_price(
        ids,
        vs_currencies
    )

    exchange_rate = await Count.count_send_value(
        get_value=1,
        coin_price=coin_price,
        margin=client_buy_coin.buy_margin,
        gas=client_buy_coin.buy_gas
    )
    return exchange_rate


async def check_user_registration(
        redis_dict,
        user,
        db,
        user_uuid
):
    if user is None:

        credit_card = await db.payment_option.get_by_where(
            PaymentOption.number == redis_dict["client_credit_card_number"]
        )
        if credit_card is None:

            # return RedirectResponse("/cc_conformation_form")
            return (
                '''
                Пользователь не найден.
                Карта не зарегестрирована.
                Редирект на верификацию карты.
                '''
            )
        if credit_card.user is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Кредитная карта зарегестрированна под другим имеилом"
            )

    # Пользователь есть в бд
    if user is not None:

        credit_card = await db.payment_option.get_by_where(
            PaymentOption.number == redis_dict["client_credit_card_number"]
        )
        crypto_wallet = await db.payment_option.get_by_where(
            PaymentOption.number == redis_dict["client_crypto_wallet"]
        )
        # client_sell_currency = await db.currency.get_by_where(
        #         Currency.tikker_id == redis_dict["client_sell_tikker"]
        # )
        # client_buy_currency = await db.currency.get_by_where(
        #         Currency.tikker_id == redis_dict["client_buy_tikker_id"]
        # )

        if (
            credit_card is not None and
            credit_card.is_verified is True
        ):

            # Проверяем если кредитная карта принадлежит пользователю
            if credit_card.user is user:
                # Добавляем ордер в бд
                if (redis_dict["client_sell_currency"]["type"] ==
                        CurrencyType.Fiat):
                    # if client_sell_currency.type == CurrencyType.Fiat:
                    new_order = await db.order.new(
                        user_id=user.id,
                        user_email=redis_dict["client_email"],
                        user_cookie=user_uuid,
                        user_buy_sum=redis_dict["client_buy_value"],
                        buy_currency_id=redis_dict["client_buy_currency"]["id"],
                        # client_buy_currency.id,
                        buy_payment_option_id=crypto_wallet.id,
                        user_sell_sum=redis_dict["client_sell_value"],
                        sell_currency_id=redis_dict["client_sell_currency"]["id"],
                        # client_sell_currency.id,
                        sell_payment_option_id=credit_card.id,
                        status=Status.Approved,
                    )
                    db.session.add(new_order)
                    await db.session.flush()
                    await db.session.commit()
                    await services.redis_values.change_keys(
                        user_uuid=user_uuid,
                        order_id=new_order.id
                    )

                if (redis_dict["client_sell_currency"]["type"] ==
                        CurrencyType.Crypto):
                    new_order = await db.order.new(
                        user_id=user.id,
                        user_email=redis_dict["client_email"],
                        user_cookie=user_uuid,
                        user_buy_sum=redis_dict["client_buy_value"],
                        buy_currency_id=redis_dict["client_buy_currency"]["id"],
                        buy_payment_option_id=credit_card.id,
                        user_sell_sum=redis_dict["client_sell_value"],
                        sell_currency_id=redis_dict["client_sell_currency"]["id"],
                        sell_payment_option_id=crypto_wallet.id,
                        status=Status.Approved,
                    )
                    db.session.add(new_order)
                    await db.session.flush()
                    await db.session.commit()
                    await services.redis_values.change_keys(
                        user_uuid=user_uuid,
                        order_id=new_order.id
                    )

                # return RedirectResponse("/order")
                return (
                    "Такой пользователь существует."
                    "Кредитная карта принадлежит пользователю."
                    "Ордер создан"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="""Кредитная карта зарегестрированна
                        под другим имеилом"""
                )

        if (
            credit_card is not None and
            credit_card.is_verified is False
        ):
            # return RedirectResponse("/confirm_order")
            return (
                    "Такой пользователь существует"
                    "Кредитная карта не верифицированна"
                    "Редирект на верификацию карты"
                )

        # return RedirectResponse("/confirm_order")
        return (
            "Пользователь существует."
            "Кредитная карта и кошель не верицфицирован"
            "редирект на страницу верификации"
        )
