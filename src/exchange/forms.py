from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import RedirectResponse
from .sevices import Count
from .constants import LTC_PRICE
from .sevices import services
from .constants import MARGIN, GAS, EMAIL_QUEUE
import secrets
from config import conf
from database.db import Database as db

forms_router = APIRouter(
    prefix="/forms",
    tags=["forms"]
)


# Форма для обмена LTC/SBERRUB
@forms_router.post("/ltc_sberrub")
async def order_crypto_fiat(
    send_value: int = Form(default=0),
    get_value: int = Form(default=0),
    email: str = Form(),
    cc_num: str = Form(),
    cc_holder: str = Form(),
):
    print(f"маржа: {MARGIN}")
    print(f"Стоимость за перевод: {GAS}")
    if send_value != 0:
        try:
            get_value = await Count.count_get_value(
                send_value=send_value,
                coin_price=await LTC_PRICE,
                margin=MARGIN,
                gas=GAS,
            )
            print(f"Сумма рублей за лтс: {get_value}")
        except SyntaxError:
            print("Error in send value")
    if send_value == 0:
        try:
            send_value = await Count.count_send_value(
                get_value=get_value,
                coin_price=await LTC_PRICE,
                margin=MARGIN,
                gas=GAS,
            )
        except SyntaxError:
            print("Error in send value")

    try:
        await services.redis_values.set_email_values(
            email=email,
            send_value=send_value,
            get_value=get_value,
            cc_num=cc_num,
            cc_holder=cc_holder,
        )
    except SyntaxError:
        print("Redis Error")
    try:
        await EMAIL_QUEUE.put(email)
    except SyntaxError:
        print("EmailQueue error")
    print("succes")
    return RedirectResponse("/confirm_cc")


# Форма для верификации карты по фото
@forms_router.post("/confirm_cc_form")
async def confirm_cc(
    cc_image: UploadFile,
):
    email = await EMAIL_QUEUE.get()
    does_exist = await services.redis_values.redis_conn.exists(f'{email}')
    # Проверяем есть ли ключи в реддисе
    if does_exist != 1:
        # Меняем статус ордера на время вышло
        return "Время вышло"
    # Проверяем формат картинки
    cc_image_name = cc_image.filename
    extension = cc_image_name.split(".")[1]

    if extension not in ["png", "jpg"]:
        return {"status": "error", "detail": "File extension is not allowed"}

    # Создаем новое название картинки,
    # записываем в файл и отправляем на Яндекс диск
    new_file_name = f"{secrets.token_hex(10)}.{extension}"
    cc_image_content = await cc_image.read()

    with open(new_file_name, "wb") as file:
        file.write(cc_image_content)

    await conf.image_storage.build_image_storage.upload(
        new_file_name, "/exchange"
    )
    await conf.image_storage.build_image_storage.close()

    # Достаем из редиса список с данными ордера
    # Добавляем все значения в базу на PendingOrder модель для админа
    # Меняем статус ордера в модели ордер на в процессе

    cc_holder, cc_num, get_value, send_value = (
        await services.redis_values.redis_conn.lrange(email, 0, -1)
    )

    new_pending_order = await db.pending_order.new(
        email=email,
        send_value=send_value,
        get_value=get_value,
        cc_num=cc_num,
        cc_holder=cc_holder,
        cc_image_name=new_file_name,
    )
    await db.session.commit(new_pending_order)
    return RedirectResponse("/pending")
