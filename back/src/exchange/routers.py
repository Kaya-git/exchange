import asyncio
from decimal import Decimal
from typing import Annotated

from currencies.models import Currency
from database.db import Database, get_async_session
from enums.models import ReqAction, Status
from fastapi import (
    APIRouter, Depends, Form, Path, UploadFile, BackgroundTasks
)
from sevices import services
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User

from .handlers import (
    add_or_get_po, calculate_totals, check_form_fillment,
    check_user_registration, find_exchange_rate,
    generate_pass, get_password_hash,
    start_time, ya_save_passport_photo
)

from background_tasks.handlers import controll_order


exchange_router = APIRouter(
    prefix="/api/exchange",
    tags=["Роутер обмена"]
)


@exchange_router.get("/{client_sell_tikker}/{client_buy_tikker}")
async def get_exchange_rates(
    client_sell_tikker: Annotated[
        str, Path(title="The Tikker of the coin client sell")
    ],
    client_buy_tikker: Annotated[
        str, Path(title="The Tikker of the coin client buy")
    ],
    session: AsyncSession = Depends(get_async_session)
):
    """ Отдает словарь со стоимостью запрашиваемой пары, тикерами,
    иконками, максимальными и минимальными значениями """
    db = Database(session=session)

    client_sell_coin = await db.currency.get_by_where(
        Currency.tikker == client_sell_tikker
    )
    client_buy_coin = await db.currency.get_by_where(
        Currency.tikker == client_buy_tikker
    )

    exchange_rate = await find_exchange_rate(
            client_sell_coin, client_buy_coin
        )

    exchange_dict = {}

    exchange_dict["give"] = client_sell_coin
    exchange_dict["get"] = client_buy_coin
    exchange_dict["exchange_rate"] = exchange_rate

    return exchange_dict


# Страница для формы обмена
@exchange_router.post("/exchange_form")
async def fill_order_form(
    background_tasks: BackgroundTasks,
    client_sell_value: Decimal = Form(default=0),
    client_sell_tikker: str = Form(),
    client_buy_value: Decimal = Form(default=0),
    client_buy_tikker: str = Form(),
    client_email: str = Form(),
    client_crypto_wallet: str = Form(),
    client_credit_card_number: str = Form(),
    client_cc_holder: str = Form(),
    user_uuid: str | None = Form(),
    session: AsyncSession = Depends(get_async_session)
):
    """ Форма для создания заявки"""

    # Номер ендпоинта в цепочке заявки
    END_POINT_NUMBER = 1

    # Экземпляр обстракции для обращения к бд
    db = Database(session=session)

    # Формируем словарь с данными
    form_voc = {
        "client_sell_value": client_sell_value,
        "client_sell_tikker": client_sell_tikker,
        "client_buy_value": client_buy_value,
        "client_buy_tikker": client_buy_tikker,
        "client_email": client_email,
        "client_crypto_wallet": client_crypto_wallet,
        "client_credit_card_number": client_credit_card_number,
        "client_cc_holder": client_cc_holder,
        "user_uuid": user_uuid
    }

    # Проверяем наполненость формы, либо отдаем ошибку
    if await check_form_fillment(form_voc):

        # Просчитываем стоимость валюты с учетом коммисий и
        # стоимости за перевод
        client_sell_coin = await db.currency.get_by_where(
            Currency.tikker == client_sell_tikker
        )
        client_buy_coin = await db.currency.get_by_where(
            Currency.tikker == client_buy_tikker
        )
        coin_price = await find_exchange_rate(
            client_sell_coin, client_buy_coin
        )

        # Определяем какую строчку в форме заполнил пользователь и
        # просчитываем стоимость
        totals = await calculate_totals(
            client_sell_coin,
            client_buy_coin,
            coin_price,
            client_sell_value,
            client_buy_value
        )

        # Сохраняем переменные в редис под ключем = uuid пользователя
        await services.redis_values.set_order_info(
            user_uuid=user_uuid,
            end_point_number=END_POINT_NUMBER,
            client_email=client_email,
            client_sell_value=totals["client_sell_value"],
            client_sell_tikker=client_sell_tikker,
            client_buy_value=totals["client_buy_value"],
            client_buy_tikker=client_buy_tikker,
            client_credit_card_number=client_credit_card_number,
            client_cc_holder=client_cc_holder,
            client_crypto_wallet=client_crypto_wallet,
        )

        # Выставляем время жизни заявки до дальнейшего перехода по цепочке
        await services.redis_values.set_ttl(
            user_uuid=user_uuid,
            time_out=50
        )

        # Запускаем фоновую задачу на котроль заявки
        background_tasks.add_task(
            controll_order,
            user_uuid,
            db
        )

        # Отдаем время старт заявки для запуска таймера на фронте
        return await start_time()


@exchange_router.post("/confirm_order")
async def confirm_order(
    user_uuid: str | None = Form(),
    async_session: AsyncSession = Depends(get_async_session)
):
    """ Отправляет пользователю данные заявки на проверку"""

    # Номер ендпоинта в цепочке заявки
    END_POINT_NUMBER = 2

    # Экземпляр обстракции для обращения к бд
    db = Database(session=async_session)

    # Проверяем существование ключа в редисе
    await services.redis_values.check_existance(
        user_uuid=user_uuid
    )

    # Выставляем следующий номер эндпоинта в роутере
    await services.redis_values.change_redis_router_num(
        user_uuid=user_uuid,
        router_num=END_POINT_NUMBER
    )

    # Декодируем значения редиса в пайтоновские типы
    redis_dict = await services.redis_values.decode_values(
        user_uuid=user_uuid,
        db=db
    )

    # Выставляем таймер на
    await services.redis_values.set_ttl(
        user_uuid=user_uuid,
        time_out=120
    )

    # Возвращаем значения для подтверждения
    return redis_dict


@exchange_router.post("/confirm_button")
async def confirm_button(
    user_uuid: str | None = Form(),
    async_session: AsyncSession = Depends(get_async_session)
):

    # Номер ендпоинта в цепочке заявки
    END_POINT_NUMBER = 3

    # Экземпляр обстракции для обращения к бд
    db = Database(session=async_session)

    # Проверяем существование ключа в редисе
    await services.redis_values.check_existance(user_uuid)

    # Декодируем значения редиса в пайтоновские типы
    redis_dict = await services.redis_values.decode_values(
        user_uuid=user_uuid,
        db=db
        )

    # Выставляем следующий номер эндпоинта в роутере
    await services.redis_values.change_redis_router_num(
        user_uuid=user_uuid,
        router_num=END_POINT_NUMBER
    )

    # Проверяем зарегистрирован пользователь или нет
    registration_status = await check_user_registration(
        redis_dict=redis_dict,
        db=db,
        user_uuid=user_uuid,
        end_point_number=END_POINT_NUMBER
    )

    # Выставляем таймер на
    await services.redis_values.set_ttl(
        user_uuid=user_uuid,
        time_out=120
    )

    return registration_status


# Отправляем фото паспорта на верификацию админу
@exchange_router.post("/cc_conformation_form")
async def confirm_cc(
    cc_image: UploadFile,
    user_uuid: str | None = Form(),
    session: AsyncSession = Depends(get_async_session)
):
    """ Форма для отправки фотографии с картой"""

    # Номер ендпоинта в цепочке заявки
    END_POINT_NUMBER = 4

    # Экземпляр обстракции для обращения к бд
    db = Database(session=session)

    # Проверяем существование ключа в редисе
    await services.redis_values.check_existance(user_uuid)

    # Отправляем фотографию в Яндекс Диск
    new_file_name = await ya_save_passport_photo(cc_image)

    # Декодируем значения редиса в пайтоновские типы
    redis_dict = await services.redis_values.decode_values(
        user_uuid=user_uuid,
        db=db
    )

    # Проверяем существует ли пользователь с данным мылом,
    # если нет создаем нового пользователя по email ордера с пустым паролем и
    # возвращаем его из бд

    # Находим пользователя по email
    user = await db.user.get_by_where(
        User.email == redis_dict["client_email"]
    )

    # Если пользователя нет, регистрируем нового, со сгенерированным паролем
    if user is None:

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

    # Добавляем новые способы оплаты пользователю
    p_o_dict = await add_or_get_po(
        db, redis_dict,
        user, new_file_name
    )

    # Записываем новый ордер на обмен в базу данных
    new_order = await db.order.new(
        user_id=user.id,
        user_email=redis_dict["client_email"],
        user_cookie=user_uuid,
        user_buy_sum=redis_dict["client_buy_value"],
        buy_currency_id=redis_dict["client_buy_currency"]["id"],
        buy_payment_option_id=p_o_dict["client_buy_payment_option"]["id"],
        user_sell_sum=redis_dict["client_sell_value"],
        sell_currency_id=redis_dict["client_sell_currency"]["id"],
        sell_payment_option_id=p_o_dict["client_sell_payment_option"]["id"],
        status=Status.верификация_карты,
    )
    db.session.add(new_order)
    await db.session.flush()

    # Добавляем ордер в оповещение администратору
    new_pending = await db.pending_admin.new(
        order_id=new_order.id,
        req_act=ReqAction.верифицировать_клиента
    )
    db.session.add(new_pending)
    await db.session.flush()
    await db.session.commit()

    # Заменить список с информацией в редисе на айди ордера
    await services.redis_values.change_keys(
                    user_uuid=user_uuid,
                    order_id=new_order.id,
                    user_id=user.id,
                    router_num=END_POINT_NUMBER
    )

    # Выставляем таймер на время жизни заявки
    await services.redis_values.set_ttl(
        user_uuid=user_uuid,
        time_out=120
    )

    return True


@exchange_router.post("/await")
async def conformation_await(
    user_uuid: str | None = Form(),
    async_session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Запускает паралельно задачу на отслеживание
    смены статуса верификации пользователя """

    # Номер ендпоинта в цепочке заявки
    END_POINT_NUMBER = 5

    # Экземпляр обстракции для обращения к бд
    db = Database(session=async_session)

    # Проверяем существование ключа в редисе
    await services.redis_values.check_existance(user_uuid)

    # Выставляем следующий номер эндпоинта в роутере
    await services.redis_values.change_redis_router_num(
        user_uuid=user_uuid,
        router_num=END_POINT_NUMBER
    )

    # Создаем таск на пулинг актуального статуса верификации кредитной карты
    return await asyncio.create_task(
        services.db_paralell.conformation_await(
            db,
            user_uuid
        )
    )


@exchange_router.post("/order")
async def requisites(
    async_session: AsyncSession = Depends(get_async_session),
    user_uuid: str | None = Form(),
):
    """ Отдает данные для перевода средств """

    # Номер ендпоинта в цепочке заявки
    END_POINT_NUMBER = 6

    # Экземпляр обстракции для обращения к бд
    db = Database(session=async_session)

    # Проверяем существование ключа в редисе
    await services.redis_values.check_existance(user_uuid)

    # Выставляем следующий номер эндпоинта в роутере
    await services.redis_values.change_redis_router_num(
        user_uuid=user_uuid,
        router_num=END_POINT_NUMBER
    )

    # Достаем из редиса номер заявки
    order_id = await services.redis_values.get_order_id(
        user_uuid
    )

    # Находим в платежных средствах сервиса актуальный способ оплаты
    service_payment_option = await db.service_payment_option.spo_equal_sp(
        order_id
    )

    # Выставляем таймер на время жизни заявки
    await services.redis_values.set_ttl(
        user_uuid=user_uuid,
        time_out=3600
    )

    return {
            "order_id": order_id,
            "requisites_num": service_payment_option.number,
            "holder": service_payment_option.holder
        }


@exchange_router.post("/payed")
async def payed_button(
    async_session: AsyncSession = Depends(get_async_session),
    user_uuid: str | None = Form(),
):
    """ Кнопка подтверждения оплаты пользователя
    запускает паралельно задачу на отслеживание изменения стасу ордера """

    # Номер ендпоинта в цепочке заявки
    END_POINT_NUMBER = 7

    # Экземпляр обстракции для обращения к бд
    db = Database(session=async_session)

    # Проверяем существование ключа в редисе
    await services.redis_values.check_existance(user_uuid)

    # Выставляем следующий номер эндпоинта в роутере
    await services.redis_values.change_redis_router_num(
        user_uuid=user_uuid,
        router_num=END_POINT_NUMBER
    )
    # Достаем из редиса номер заявки
    order_id = await services.redis_values.get_order_id(
        user_uuid
    )
    # Достаем из редиса номер пользователя
    user_id = await services.redis_values.get_user_id(
        user_uuid
    )
    # Добавляем актуальную заявку
    await db.pending_admin.new(
        order_id=order_id,
        req_act=ReqAction.верифицировать_транзакцию
    )
    await db.session.commit()

    # Обновляем статус заявки
    await db.order.order_status_update(
        new_status=Status.проверка_оплаты,
        order_id=order_id
    )
    # Создаем таск на пулинг подтверждения оплаты от сервиса
    task = asyncio.create_task(services.db_paralell.payed_button_db(
            db=db,
            user_uuid=user_uuid,
            order_id=order_id,
            user_id=user_id
        )
    )

    return await task
