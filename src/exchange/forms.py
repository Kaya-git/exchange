from fastapi import APIRouter, Form, UploadFile, Cookie, Depends
from fastapi.responses import RedirectResponse
import os
from .sevices import Count
from .constants import LTC_RUB_PRICE
from .sevices import services
from .constants import MARGIN, GAS
import secrets
from config import conf
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


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
    cwallet: str = Form(),
    cc_num: str = Form(),
    cc_holder: str = Form(),
    user_id: str = Cookie(),
):
    print(f"куки: {user_id}")
    print(f"маржа: {MARGIN}")
    print(f"Стоимость за перевод: {GAS}")
    if send_value != 0:
        try:
            get_value = await Count.count_get_value(
                send_value=send_value,
                coin_price=await LTC_RUB_PRICE,
                margin=MARGIN,
                gas=GAS,
            )
        except SyntaxError:
            print("Error in get value")
    if send_value == 0:
        try:
            send_value = await Count.count_send_value(
                get_value=get_value,
                coin_price=await LTC_RUB_PRICE,
                margin=MARGIN,
                gas=GAS,
            )
        except SyntaxError:
            print("Error in send value")

    try:
        await services.redis_values.set_order_info(
            cookies_id=user_id,
            email=email,
            send_value=send_value,
            send_curr="SBERRUB",
            get_value=get_value,
            get_curr="LTC",
            cc_num=cc_num,
            cc_holder=cc_holder,
            wallet_num=cwallet,
        )
    except SyntaxError:
        print("Redis Error")
    return "Redis - OK"
    # return RedirectResponse("/confirm")


# Форма для верификации карты по фото
@forms_router.post("/confirm_cc_form")
async def confirm_cc(
    cc_image: UploadFile,
    user_id: str = Cookie(),
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
        wallet_num,
        cc_holder,
        cc_num,
        get_curr,
        get_value,
        send_curr,
        send_value,
        email
    ) = await services.redis_values.redis_conn.lrange(user_id, 0, -1)

    wallet_num = str(wallet_num, 'UTF-8')
    cc_holder = str(cc_holder, 'UTF-8')
    cc_num = str(cc_num, 'UTF-8')
    get_curr = str(get_curr, 'UTF-8')
    get_value = float(get_value)
    send_curr = str(send_curr, 'UTF-8')
    send_value = float(send_value)
    email = str(email, 'UTF-8')

    print(f'{wallet_num}: {type(wallet_num)},\n'
          f'{cc_holder}: {type(cc_holder)},\n'
          f'{cc_num}: {type(cc_num)},\n'
          f'{get_curr}: {type(get_curr)},\n'
          f'{get_value}: {type(get_value)},\n'
          f'{send_curr}: {type(send_curr)},\n'
          f'{send_value}: {type(send_value)},\n'
          f'{email}: {type(email)},\n')

    db = Database(session=session)

    payment_from = await db.payment_option.new(
        currency=send_curr,
        amount=send_value,
        cc_num_x_wallet=cc_num,
        cc_holder=cc_holder,
        image_name=new_file_name,
        user_id=user_id,
    )

    payment_to = await db.payment_option.new(
        currency=get_curr,
        amount=get_value,
        cc_num_x_wallet=wallet_num,
        user_id=user_id
    )
    db.session.add_all([payment_from, payment_to])
    await db.session.commit()
    print(" Payments added")

    pending_order = await db.pending_order.new(
        email=email,
        payment_from=payment_from.id,
        payment_to=payment_to.id,
        user_uuid=user_id,
    )
    db.session.add(pending_order)
    await db.session.commit()
    return "Pending order created"
    # return RedirectResponse("/exchange/await")
