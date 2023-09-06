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
from database.models import PaymentPointer, PaymentBelonging


forms_router = APIRouter(
    prefix="/forms",
    tags=["forms"]
)


# Форма для обмена
@forms_router.post("/exchange_form")
async def order_crypto_fiat(
    client_send_value: int = Form(default=0),
    client_send_currency_id: int = Form(),
    client_get_value: int = Form(default=0),
    client_get_currency_id: int = Form(),
    client_email: str = Form(),
    client_crypto_wallet: str = Form(),
    client_cc_num: str = Form(),
    client_cc_holder_name: str = Form(),
    user_id: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session),
):
    if client_send_currency_id in CRYPTO_ID_TIKKERS:
        send_tikker = CRYPTO_ID_TIKKERS[f"{client_send_currency_id}"]
        get_tikker = FIAT_ID_TIKKERS[f"{client_get_currency_id}"]
        parser_tikker = f"{send_tikker}{get_tikker}"

    if client_send_currency_id in FIAT_ID_TIKKERS:
        send_tikker = FIAT_ID_TIKKERS[client_send_currency_id]
        get_tikker = CRYPTO_ID_TIKKERS[client_get_currency_id]
        parser_tikker = f"{get_tikker}{send_tikker}"

    else:
        raise ValueError("Айди тикера вне словаря")
    # -----

    db = Database(session=session)
    commissions = await db.commissions.get(1)
    coin_price = await find_price(parser_tikker)
    if client_send_value != 0:
        try:
            client_get_value = await Count.count_get_value(
                send_value=client_send_value,
                coin_price=coin_price,
                margin=commissions.margin,
                gas=commissions.gas,
            )
        except SyntaxError:
            print("Error in get value")
    if client_send_value == 0:
        try:
            client_send_value = await Count.count_send_value(
                get_value=client_get_value,
                coin_price=coin_price,
                margin=commissions.margin,
                gas=commissions.gas,
            )
        except SyntaxError:
            print("Error in send value")

    try:
        await services.redis_values.set_order_info(
            user_id=user_id,
            client_email=client_email,
            client_send_value=client_send_value,
            send_tikker_id=client_send_currency_id,
            client_get_value=client_get_value,
            get_tikker_id=client_get_currency_id,
            client_cc_num=client_cc_num,
            client_cc_holder_name=client_cc_holder_name,
            client_crypto_wallet=client_crypto_wallet,
        )
    except SyntaxError:
        print("Redis Error")
    return "Redis - OK"
    # return RedirectResponse("/confirm")


# Форма для верификации карты по фото
@forms_router.post("/cc_conformation_form")
async def confirm_cc(
    cc_image: UploadFile,
    user_id: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session)
):
    does_exist = await services.redis_values.redis_conn.exists(user_id)
    # Проверяем есть ли ключи в реддисе
    if does_exist != 1:
        # Меняем статус ордера на время вышло
        return "Время вышло"
    # Проверяем формат картинки
    cc_image_name = cc_image.filename
    extension = cc_image_name.split(".")[1]
    print(extension)
    if extension not in ["png", "jpg", "JPG"]:
        return {"status": "error", "detail": "File extension is not allowed"}

    # Создаем новое название картинки,
    # записываем в файл и отправляем на Яндекс диск
    new_file_name = f"{secrets.token_hex(10)}.{extension}"
    print(new_file_name)
    cc_image_content = await cc_image.read()

    with open(new_file_name, "wb") as file:
        file.write(cc_image_content)

    image_storage = await conf.image_storage.build_image_storage()

    await image_storage.upload(new_file_name, f"/exchange/{new_file_name}")
    await image_storage.close()
    os.remove(f"{new_file_name}")

    # Достаем из редиса список с данными ордера
    # Добавляем все значения в базу на PendingOrder модель для админа
    # Меняем статус ордера в модели ордер на в процессе

    (
        client_crypto_wallet,
        client_cc_holder_name,
        client_cc_num,
        get_tikker_id,
        client_get_value,
        send_tikker_id,
        client_send_value,
        client_email
    ) = await services.redis_values.redis_conn.lrange(user_id, 0, -1)

    client_crypto_wallet = str(client_crypto_wallet, 'UTF-8')
    client_cc_holder_name = str(client_cc_holder_name, 'UTF-8')
    client_cc_num = str(client_cc_num, 'UTF-8')
    get_tikker_id = int(get_tikker_id, 'UTF-8')
    client_get_value = float(client_get_value)
    send_tikker_id = int(send_tikker_id, 'UTF-8')
    client_send_value = float(client_send_value)
    client_email = str(client_email, 'UTF-8')

    db = Database(session=session)

    new_order = await db.pending_order.new(
        email=client_email,
        give_amount=client_send_value,
        get_amount=client_get_value,
        user_uuid=user_id,
        give_currency_id=send_tikker_id,
        get_currency_id=get_tikker_id,
    )

    db.session.add(new_order)

    if send_tikker_id not in CRYPTO_ID_TIKKERS:
        payment_from = await db.payment_option.new(
            cc_num_x_wallet=client_cc_num,
            cc_holder=client_cc_holder_name,
            image_name=new_file_name,
            payment_point=PaymentPointer.From,
            clien_service_belonging=PaymentBelonging.Client,
            currency_id=send_tikker_id,
            pending_order_id=new_order.id,
        )
        payment_to = await db.payment_option.new(
            cc_num_x_wallet=client_crypto_wallet,
            image_name=new_file_name,
            payment_point=PaymentPointer.To,
            clien_service_belonging=PaymentBelonging.Client,
            currency_id=get_tikker_id,
            pending_order_id=new_order.id,
        )
        db.session.add_all([payment_from, payment_to])
        await db.session.commit()
        print(" Payments added")
        return "Pending order created"

    if send_tikker_id in CRYPTO_ID_TIKKERS:
        payment_to = await db.payment_option.new(
            cc_num_x_wallet=client_cc_num,
            cc_holder=client_cc_holder_name,
            image_name=new_file_name,
            payment_point=PaymentPointer.From,
            clien_service_belonging=PaymentBelonging.Client,
            currency_id=send_tikker_id,
            pending_order_id=new_order.id,
        )
        payment_from = await db.payment_option.new(
            cc_num_x_wallet=client_crypto_wallet,
            image_name=new_file_name,
            payment_point=PaymentPointer.To,
            clien_service_belonging=PaymentBelonging.Client,
            currency_id=get_tikker_id,
            pending_order_id=new_order.id,
        )
        db.session.add_all([payment_from, payment_to])
        await db.session.commit()
        print(" Payments added")
        return "Pending order created"
    else:
        raise ValueError("send_tikker_id not in any currency dict")
#     # return RedirectResponse("/exchange/await")
