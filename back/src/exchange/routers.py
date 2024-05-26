import asyncio
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form, Path, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from background_tasks.handlers import controll_order
from currencies.models import Currency
from database.db import Database, get_async_session
from enums.models import ReqAction, Status
from sevices import services
from pendings.models import PendingAdmin
from .handlers import (add_or_get_po, calculate_totals, check_form_fillment,
                       check_user_registration, find_exchange_rate, start_time,
                       ya_save_passport_photo)
import logging
from enums.models import CurrencyType


LOGGER = logging.getLogger(__name__)


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

    # Экземпляр обстракции для обращения к бд
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
            time_out=600
        )
        await services.redis_values.set_ttl(
            user_uuid=f"{user_uuid}_data",
            time_out=600
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
        time_out=600
    )

    await services.redis_values.set_ttl(
            user_uuid=f"{user_uuid}_data",
            time_out=600
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
        time_out=600
    )
    await services.redis_values.set_ttl(
            user_uuid=f"{user_uuid}_data",
            time_out=600
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

    LOGGER.info(f"UUID пользователя {user_uuid}")

    # Номер ендпоинта в цепочке заявки
    END_POINT_NUMBER = 4

    # Экземпляр обстракции для обращения к бд
    db = Database(session=session)

    # Проверяем существование ключа в редисе
    await services.redis_values.check_existance(user_uuid)

    # Отправляем фотографию в Яндекс Диск
    new_file_name = await ya_save_passport_photo(cc_image)

    # Получаем пользователя
    user_id = await services.redis_values.get_user_id(user_uuid=user_uuid)

    # Декодируем значения редиса в пайтоновские типы
    redis_dict = await services.redis_values.decode_values(
        user_uuid=user_uuid,
        db=db,
        end_point_number=END_POINT_NUMBER
        )

    # Добавляем новые способы оплаты пользователю
    p_o_dict = await add_or_get_po(
        db=db,
        redis_voc=redis_dict,
        user_id=user_id,
        new_file_name=new_file_name
    )

    # Получаем номер
    order_id = await services.redis_values.get_order_id(user_uuid=user_uuid)

    LOGGER.info(f"Номер заявки: {order_id}, тип {type(order_id)}")

    await db.order.update_pos(
        order_id=order_id,
        po_buy=p_o_dict["client_buy_payment_option"]["id"],
        po_sell=p_o_dict["client_sell_payment_option"]["id"]
    )

    if redis_dict["client_sell_currency"]["type"] == CurrencyType.Фиат:
        fiat_id = p_o_dict["client_sell_payment_option"]["id"]
    if redis_dict["client_buy_currency"]["type"] == CurrencyType.Фиат:
        fiat_id = p_o_dict["client_buy_payment_option"]["id"]

    LOGGER.info(f"ID записи для верифкации: {fiat_id}, тип {type(fiat_id)}")

    # Добавляем ордер в оповещение администратору
    new_pending = await db.pending_admin.new(
        order_id=order_id,
        req_act=ReqAction.верифицировать_клиента,
        payment_option_id=fiat_id
    )

    # Выставляем следующий номер эндпоинта в роутере
    await services.redis_values.change_redis_router_num(
        user_uuid=user_uuid,
        router_num=END_POINT_NUMBER
    )

    db.session.add(new_pending)
    await db.session.flush()
    await db.session.commit()

    # Выставляем таймер на время жизни заявки
    await services.redis_values.set_ttl(
        user_uuid=user_uuid,
        time_out=600
    )
    await services.redis_values.set_ttl(
            user_uuid=f"{user_uuid}_data",
            time_out=600
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
) -> dict:
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
        time_out=900
    )
    await services.redis_values.set_ttl(
            user_uuid=f"{user_uuid}_data",
            time_out=900
    )

    return {
            "order_id": order_id,
            "requisites_num": service_payment_option.number,
            "holder": service_payment_option.holder
        }


@exchange_router.post("/payed")
async def payed_button(
    background_tasks: BackgroundTasks,
    async_session: AsyncSession = Depends(get_async_session),
    user_uuid: str | None = Form(),
):
    """ Кнопка подтверждения оплаты пользователя
    запускает паралельно задачу на отслеживание изменения стасу ордера """

    logging.info("Клиент произвел оплату")

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
    # user_id = await services.redis_values.get_user_id(
    #     user_uuid
    # )
    pending = await db.pending_admin.get_by_where(
        PendingAdmin.order_id == order_id
    )
    if pending is None:
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

    # Выставляем таймер на время жизни заявки
    await services.redis_values.set_ttl(
        user_uuid=user_uuid,
        time_out=900
    )
    await services.redis_values.set_ttl(
            user_uuid=f"{user_uuid}_data",
            time_out=900
    )
