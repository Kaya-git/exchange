from fastapi import APIRouter, Cookie, Depends, Form, UploadFile, Path, HTTPException, status
from fastapi.responses import RedirectResponse
from sevices import services
from database.db import Database, get_async_session
from binance_parser import find_price
from currencies.models import Currency
from orders.models import Order
from enums.models import Status, CurrencyType, ReqAction
from users.models import User
from payment_options.models import PaymentOption
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from decimal import Decimal
from sevices import Count
from .handlers import (
    check_form_fillment,
    create_tikker_for_binance,
    ya_save_passport_photo,
    redis_discard,
    add_or_get_po,
    send_email,
    generate_pass,
    get_password_hash,
    calculate_totals,
    find_exchange_rate,
    check_user_registration
)
from typing import Annotated


exchange_router = APIRouter(
    prefix="/exchange",
    tags=["Роутер обмена"]
)

@exchange_router.get("/{client_sell_tikker_id}/{client_buy_tikker_id}")
async def get_exchange_rates(
    client_sell_tikker_id: Annotated[int, Path(title="The ID of the coin client sell")],
    client_buy_tikker_id: Annotated[int, Path(title="The ID of the coin client buy")],
    session: AsyncSession = Depends(get_async_session)
):
    """ Отдает словарь со стоимостью запрашиваемой пары, тикерами, иконками, максимальными и минимальными значениями """
    db = Database(session=session)
    
    client_sell_coin = await db.currency.get_by_where(
        Currency.tikker_id == client_sell_tikker_id
    )
    exchange_dict = {}
    get = []
    if client_sell_coin.type == CurrencyType.Fiat:
        client_buy_coin_list = await db.currency.get_many(
            whereclause=(Currency.type == CurrencyType.Crypto)
        )

        for client_buy_coin in client_buy_coin_list:
            client_buy_coin_dict = client_buy_coin.__dict__
            exchange_rate = await find_exchange_rate(client_sell_coin, client_buy_coin)
            client_buy_coin_dict["exchange_rate"] = exchange_rate
            get.append(client_buy_coin_dict)

    if client_sell_coin.type == CurrencyType.Crypto:
        client_buy_coin_list = await db.currency.get_many(
            whereclause=(Currency.type == CurrencyType.Crypto)
        )
        
        for client_buy_coin in client_buy_coin_list:
            client_buy_coin_dict = client_buy_coin.__dict__
            exchange_rate = await find_exchange_rate(client_sell_coin, client_buy_coin)
            client_buy_coin_dict["exchange_rate"] = exchange_rate
            get.append(client_buy_coin)

    exchange_dict["give"] = client_sell_coin
    exchange_dict["get"] = get

    return exchange_dict


# Заполняем форму для обмена и передаем ее в редис
@exchange_router.post("/exchange_form")
async def fill_order_form(
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
    """ Форма для заполнения заказа на обмен """
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
    # Проверяем наполненость формы
    await check_form_fillment(form_voc)

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
    totals = await calculate_totals(parser_link_voc, coin_price, client_sell_value, client_buy_value)

    # Сохраняем переменные в редис под ключем = uuid пользователя
    await services.redis_values.set_order_info(
            user_uuid=user_uuid,
            client_email=client_email,
            client_sell_value=totals["client_sell_value"],
            client_sell_tikker_id=client_sell_tikker_id,
            client_buy_value=totals["client_buy_value"],
            client_buy_tikker_id=client_buy_tikker_id,
            client_credit_card_number=client_credit_card_number,
            client_cc_holder=client_cc_holder,
            client_crypto_wallet=client_crypto_wallet,
            client_sell_currency_po=parser_link_voc["client_sell_currency_po"],
            client_buy_currency_po=parser_link_voc["client_buy_currency_po"]
    )
    return "Redis - OK"
    # return RedirectResponse("/confirm_order")


@exchange_router.post("/confirm_order")
async def confirm_order(
    user_uuid: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session)
):
    """ Отправляет пользователю заполненые данные для подтверждения заказа """
    db = Database(session=async_session)

    # Проверяем есть ли ключи в реддисе и забираем значения
    does_exist = await services.redis_values.redis_conn.exists(user_uuid)
    if does_exist != 1:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Время вышло. Необходимо создать новый обмен"
        )
    redis_dict = await redis_discard(
        user_uuid=user_uuid,
        db=db
        )
    # Возвращаем значения для подтверждения
    return redis_dict


@exchange_router.get("/confirm_button")
async def confirm_button(
    user_uuid: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)

    # Проверяем есть ли ключи в реддисе и забираем значения
    does_exist = await services.redis_values.redis_conn.exists(user_uuid)
    if does_exist != 1:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Время вышло. Необходимо создать новый обмен"
        )
    redis_dict = await redis_discard(
        user_uuid=user_uuid,
        db=db
        )
    # Проверяем зарегестрировани ли пользователь и
    # верифицирована ли его банковская карта и
    user = await db.user.get_by_where(
        User.email == redis_dict["client_email"]
    )

    return await check_user_registration(
        redis_dict, user,
        db, user_uuid
    )
    

# Отправляем фото паспорта на верификацию админу
@exchange_router.post("/cc_conformation_form")
async def confirm_cc(
    cc_image: UploadFile,
    user_uuid: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session)
):
    """ Форма для отправки фотографии подтверждения """
    db = Database(session=session)

    # Проверяем есть ли ключи в реддисе
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

        new_password = await generate_pass()
        hashed_password = await get_password_hash(new_password)

        user = await db.user.new(
            email=redis_voc["client_email"],
            hashed_password=hashed_password
        )
        db.session.add(user)
        await db.session.flush()
        await send_email(
            recepient_email=redis_voc["client_email"],
            generated_pass=new_password
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

    # Добавляем ордер в оповещение администратору
    new_pending = await db.pending_admin.new(
        order_id=new_order.id,
        req_act=ReqAction.VerifyNewOrder
    )
    db.session.add(new_pending)
    await db.session.flush()

    # Заменить список с информацией в редисе на айди ордера
    await services.redis_values.change_keys(
                    user_uuid=user_uuid,
                    order_id=new_order.id
                )

    await db.session.commit()

    return "Pending order created"
    # return RedirectResponse("/exchange/await")


@exchange_router.post("/await")
async def conformation_await(
    user_uuid: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session)
) -> RedirectResponse:
    """ Запускает паралельно задачу на отслеживание смены статуса верификации пользователя """
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
    # return RedirectResponse("/order")


@exchange_router.post("/order")
async def requisites(
    async_session: AsyncSession = Depends(get_async_session),
    user_uuid: str | None = Cookie(default=None),
):
    """ Отдает данные для перевода средств """
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

    service_payment_option = await db.service_payment_option.spo_equal_sp(order_id)

    return {
            "requisites_num": service_payment_option.number,
            "holder": service_payment_option.holder
        }


@exchange_router.post("/payed")
async def payed_button(
    async_session: AsyncSession = Depends(get_async_session),
    user_uuid: str | None = Cookie(default=None),
):
    """ Кнопка подтверждения оплаты пользователя 'запускает паралельно задачу на отслеживание изменения стасу ордера' """
    db = Database(session=async_session)

    # Проверяем редис на наличие ключей,
    # если исчезли, то ставим статус ордера на просрок
    does_exist = await services.redis_values.redis_conn.exists(user_uuid)
    order_id = await services.redis_values.redis_conn.lindex(
        user_uuid,
        0
    )
    order_id = int(order_id)

    payed_order = await db.pending_admin.new(
        order_id=order_id,
        req_act=ReqAction.VerifyTransaction
    )
    await db.session.commit()
    if not does_exist:

        timeout = await db.order.order_status_timout(order_id)

        if timeout:

            return "Время вышло, необходим новый ордер"

    task = asyncio.create_task(services.db_paralell.payed_button_db(
            db=db,
            user_uuid=user_uuid,
            order_id=order_id
        )
    )
    answer = await task
    return answer
