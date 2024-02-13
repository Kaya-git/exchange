import datetime
import secrets

import aiofiles
import aiofiles.os
from fastapi import HTTPException, status
from passlib.context import CryptContext

from config import conf
from currencies.routers import CoingekkoParamsDTO
from database.db import Database
from enums import CurrencyType, Status
from payment_options.models import PaymentOption
from price_parser.parser import CoinGekkoParser, parse_the_price
from sevices import Count, services
from users.models import User

Time = str


async def start_time() -> Time:
    return datetime.datetime.now().time()


async def generate_pass():
    return secrets.token_hex(10)


async def get_password_hash(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


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
    # Проверяем формат картинки
    cc_image_name = cc_image.filename
    extension = cc_image_name.split(".")[1]

    if extension not in ["png", "jpg", "JPG", "PNG", "jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Неподходящий формат файла'
        )

    # Создаем новое название картинки,
    # записываем в файл и отправляем на Яндекс диск
    new_file_name = f"{secrets.token_hex(10)}.{extension}"
    cc_image_content = await cc_image.read()

    async with aiofiles.open(new_file_name, "wb") as file:
        await file.write(cc_image_content)

    image_storage = await conf.image_storage.build_image_storage()

    await image_storage.upload(
        new_file_name,
        f"/exchange/{new_file_name}"
    )
    await image_storage.close()
    await aiofiles.os.remove(new_file_name)
    return new_file_name


async def add_or_get_po(
        db: Database,
        redis_voc: dict,
        user_id: int,
        new_file_name: str
):

    crypto_po = await db.payment_option.get_by_where(
        PaymentOption.number == redis_voc["client_crypto_wallet"]
    )

    fiat_po = await db.payment_option.get_by_where(
        PaymentOption.number == redis_voc["client_credit_card_number"]
    )

    if crypto_po is None and fiat_po is None:

        if redis_voc["client_sell_currency"]["type"] == CurrencyType.Фиат:

            client_sell_payment_option = await db.payment_option.new(
                currency_id=redis_voc["client_sell_currency"]["id"],
                number=redis_voc["client_credit_card_number"],
                holder=redis_voc["client_cc_holder"],
                image=new_file_name,
                user_id=user_id,
            )

            client_buy_payment_option = await db.payment_option.new(
                currency_id=redis_voc["client_buy_currency"]["id"],
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user_id,
            )

        if redis_voc["client_sell_currency"]["type"] == CurrencyType.Крипта:

            client_sell_payment_option = await db.payment_option.new(
                currency_id=redis_voc["client_sell_currency"]['id'],
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user_id,
            )

            client_buy_payment_option = await db.payment_option.new(
                currency_id=redis_voc["client_buy_currency"]["id"],
                number=redis_voc["client_credit_card_number"],
                holder=redis_voc["client_cc_holder"],
                image=new_file_name,
                user_id=user_id,
            )

        db.session.add_all(
            [client_sell_payment_option, client_buy_payment_option]
        )

    if (
        crypto_po is not None and
        fiat_po is None
    ):
        if redis_voc["client_sell_currency"]["type"] == CurrencyType.Фиат:

            client_sell_payment_option = await db.payment_option.new(
                currency_id=redis_voc["client_sell_currency"]["id"],
                number=redis_voc["client_credit_card_number"],
                holder=redis_voc["client_cc_holder"],
                image=new_file_name,
                user_id=user_id,
            )

            client_buy_payment_option = crypto_po

            db.session.add(client_sell_payment_option)

        if redis_voc["client_sell_currency"]["type"] == CurrencyType.Крипта:

            client_sell_payment_option = crypto_po

            client_buy_payment_option = await db.payment_option.new(
                currency_id=redis_voc["client_buy_currency"]["id"],
                number=redis_voc["client_credit_card_number"],
                holder=redis_voc["client_cc_holder"],
                image=new_file_name,
                user_id=user_id,
            )

            db.session.add(client_buy_payment_option)

    if (
        fiat_po is not None and
        fiat_po.user_id == user_id and
        crypto_po is None
    ):

        if redis_voc["client_sell_currency"]["type"] == CurrencyType.Фиат:

            client_sell_payment_option = fiat_po

            client_buy_payment_option = await db.payment_option.new(
                currency_id=redis_voc["client_buy_currency"]["id"],
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user_id,
            )
            db.session.add(client_buy_payment_option)

        if redis_voc["client_sell_currency"]["type"] == CurrencyType.Крипта:

            client_sell_payment_option = await db.payment_option.new(
                currency_id=redis_voc["client_sell_currency"]["id"],
                number=redis_voc["client_crypto_wallet"],
                holder=redis_voc["client_email"],
                user_id=user_id,
            )
            client_buy_payment_option = fiat_po
            db.session.add(client_sell_payment_option)

    if (
        fiat_po is not None and
        crypto_po is not None
    ):
        print(f"fiat_po.user: {fiat_po.user_id}")
        if fiat_po.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Номер карты зарегестрирован под другим имейлом"
            )

        if crypto_po.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Номер карты зарегестрирован под другим имейлом"
            )

        client_sell_payment_option = fiat_po
        client_buy_payment_option = fiat_po
    await db.session.flush()
    await db.session.commit()
    return {
            "client_sell_payment_option": client_sell_payment_option.__dict__,
            "client_buy_payment_option": client_buy_payment_option.__dict__
        }


async def calculate_totals(
        client_sell_coin,
        client_buy_coin,
        coin_price,
        client_sell_value,
        client_buy_value
):
    if client_sell_value != 0:

        if client_sell_coin.type == CurrencyType.Крипта:

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
        if client_sell_coin.type == CurrencyType.Фиат:

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

        if client_buy_coin.type == CurrencyType.Крипта:

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
        if client_buy_coin.type == CurrencyType.Фиат:

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

        coingekko_params = CoingekkoParamsDTO(
            ids=client_buy_coin.coingecko_tik,
            vs_currencies=client_sell_coin.coingecko_tik
        )

    if client_buy_coin.coingecko_tik == "rub":

        coingekko_params = CoingekkoParamsDTO(
            ids=client_sell_coin.coingecko_tik,
            vs_currencies=client_buy_coin.coingecko_tik
        )

    coin_price = await parse_the_price(
        parse_params=coingekko_params,
        parser=CoinGekkoParser()
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
        db,
        user_uuid,
        end_point_number
):

    # Берем значения пользователя в бд
    user = await db.user.get_by_where(
        User.email == redis_dict["client_email"]
    )

    # Если пользователь не зарегестрирован
    if user is None:

        # Проверяем если кредитная карта уже зарегестрирована
        credit_card = await db.payment_option.get_by_where(
            PaymentOption.number == redis_dict["client_credit_card_number"]
        )

        if credit_card is None:

            # Новая строка пароля
            new_password = await generate_pass()

            # Захешированый пароль
            hashed_password = await get_password_hash(new_password)

            # Создаем пользователя
            user = await db.user.new(
                email=redis_dict["client_email"],
                hashed_password=hashed_password,
                is_verified=True
            )
            db.session.add(user)
            await db.session.flush()

            # Отправляем пользователю новый пароль
            await services.mail.send_password(
                recepient_email=redis_dict["client_email"],
                generated_pass=new_password
            )

            # Создаем заявку
            new_order = await db.order.new(
                user_id=user.id,
                user_email=redis_dict["client_email"],
                user_cookie=user_uuid,
                user_buy_sum=redis_dict["client_buy_value"],
                buy_currency_id=redis_dict["client_buy_currency"]["id"],
                user_sell_sum=redis_dict["client_sell_value"],
                sell_currency_id=redis_dict["client_sell_currency"]["id"],
                status=Status.верификация_карты,
            )
            db.session.add(new_order)
            await db.session.flush()
            await db.session.commit()

            # Заменить список с информацией в редисе на айди ордера
            await services.redis_values.add_keys(
                user_uuid=user_uuid,
                order_id=new_order.id,
                user_id=user.id
            )

            # Выставляем следующий номер эндпоинта в роутере
            await services.redis_values.change_redis_router_num(
                user_uuid=user_uuid,
                router_num=end_point_number
            )
            return {
                "verified": False
            }

        if credit_card is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Кредитная карта зарегестрированна под другим имеилом"
            )

    # Пользователь есть в бд

    # Проверяем способы оплаты пользователя
    credit_card = await db.payment_option.get_by_where(
        PaymentOption.number == redis_dict["client_credit_card_number"]
    )
    crypto_wallet = await db.payment_option.get_by_where(
        PaymentOption.number == redis_dict["client_crypto_wallet"]
    )

    if (
        credit_card is not None and
        credit_card.is_verified is True
    ):

        # Проверяем если кредитная карта принадлежит пользователю
        if credit_card.user_id is user.id:

            # Если пользователь покупает криптовалюту
            if (redis_dict["client_sell_currency"]["type"] ==
                    CurrencyType.Фиат):

                if crypto_wallet is None:

                    new_crypto_wallet = await db.payment_option.new(
                        user_id=user.id,
                        currency_id=redis_dict["client_buy_currency"]["id"],
                        number=redis_dict["client_crypto_wallet"],
                        holder=redis_dict["client_cc_holder"]
                    )
                    db.session.add(new_crypto_wallet)
                    await db.session.flush()

                # Добавляем заявку в бд
                new_order = await db.order.new(
                    user_id=user.id,
                    user_email=redis_dict["client_email"],
                    user_cookie=user_uuid,
                    user_buy_sum=redis_dict["client_buy_value"],
                    buy_currency_id=redis_dict["client_buy_currency"]["id"],
                    buy_payment_option_id=new_crypto_wallet.id,
                    user_sell_sum=redis_dict["client_sell_value"],
                    sell_currency_id=redis_dict["client_sell_currency"]["id"],
                    sell_payment_option_id=credit_card.id,
                    status=Status.ожидание_оплаты,
                )

            # Если пользователь продает криптовалюту
            if (redis_dict["client_sell_currency"]["type"] ==
                    CurrencyType.Крипта):

                if crypto_wallet is None:

                    new_crypto_wallet = await db.payment_option.new(
                        user_id=user.id,
                        currency_id=redis_dict["client_sell_currency"]["id"],
                        number=redis_dict["client_crypto_wallet"],
                        holder=redis_dict["client_cc_holder"]
                    )
                    db.session.add(new_crypto_wallet)
                    await db.session.flush()

                # Добавляем заявку в бд
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
                    status=Status.ожидание_оплаты,
                )

            db.session.add(new_order)
            await db.session.flush()
            await db.session.commit()

            # Заменить список с информацией в редисе на айди ордера
            await services.redis_values.add_keys(
                user_uuid=user_uuid,
                order_id=new_order.id,
                user_id=user.id,
            )

            # Выставляем следующий номер эндпоинта в роутере
            await services.redis_values.change_redis_router_num(
                user_uuid=user_uuid,
                router_num=end_point_number
            )
            return {
                "verified": True
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="""Кредитная карта зарегестрированна
                    под другим имеилом"""
            )

    # Кредитная карта не верифицирована
    if (
        credit_card is not None and
        credit_card.is_verified is False
    ):
        new_order = await db.order.new(
            user_id=user.id,
            user_email=redis_dict["client_email"],
            user_cookie=user_uuid,
            user_buy_sum=redis_dict["client_buy_value"],
            buy_currency_id=redis_dict["client_buy_currency"]["id"],
            user_sell_sum=redis_dict["client_sell_value"],
            sell_currency_id=redis_dict["client_sell_currency"]["id"],
            status=Status.верификация_карты,
        )
        db.session.add(new_order)
        await db.session.flush()
        await db.session.commit()

        # Заменить список с информацией в редисе на айди ордера
        await services.redis_values.add_keys(
            user_uuid=user_uuid,
            order_id=new_order.id,
            user_id=user.id,
        )

        # Выставляем следующий номер эндпоинта в роутере
        await services.redis_values.change_redis_router_num(
            user_uuid=user_uuid,
            router_num=end_point_number
        )
        return {
            "verified": False
        }
    new_order = await db.order.new(
        user_id=user.id,
        user_email=redis_dict["client_email"],
        user_cookie=user_uuid,
        user_buy_sum=redis_dict["client_buy_value"],
        buy_currency_id=redis_dict["client_buy_currency"]["id"],
        user_sell_sum=redis_dict["client_sell_value"],
        sell_currency_id=redis_dict["client_sell_currency"]["id"],
        status=Status.верификация_карты,
    )
    db.session.add(new_order)
    await db.session.flush()
    await db.session.commit()

    # Заменить список с информацией в редисе на айди ордера
    await services.redis_values.add_keys(
        user_uuid=user_uuid,
        order_id=new_order.id,
        user_id=user.id
    )

    # Выставляем следующий номер эндпоинта в роутере
    await services.redis_values.change_redis_router_num(
        user_uuid=user_uuid,
        router_num=end_point_number
    )
    return {
        "verified": False
    }
