from fastapi import FastAPI, Response, Depends
from database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi.responses import RedirectResponse
from config import conf
from exchange import forms_router, exhange_router, menu_router
from sqladmin import Admin
from database.db import engine
from admin import (
    UserAdmin,
    ServicePaymentOptionAdmin,
    CurrencyAdmin, AdminAuth,
    PaymentOptionAdmin, ReviewAdmin,
    OrderAdmin,
)
from auth.auth import auth_backend
from auth.shemas import UserRead, UserCreate
from auth.routers import fastapi_users
from currencies.routers import currency_router
from orders.routers import orders_router
import uuid


app = FastAPI(
    title="Exchange"
)
authentication_backend = AdminAuth(
    secret_key=conf.admin_auth
)

admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend
)


admin.add_view(UserAdmin)
admin.add_view(ServicePaymentOptionAdmin)
admin.add_view(ReviewAdmin)
admin.add_view(CurrencyAdmin)
admin.add_view(PaymentOptionAdmin)
admin.add_view(OrderAdmin)


@app.get("/")
async def root(
    response: Response,
    async_session: AsyncSession = Depends(get_async_session),
):

    """Устанавливаем печеньки на пользователя"""
    cookies_uuid = uuid.uuid4()
    response.set_cookie(key="user_uuid", value=cookies_uuid)
    return cookies_uuid


app.include_router(currency_router)
app.include_router(orders_router)
app.include_router(forms_router)
app.include_router(exhange_router)
app.include_router(menu_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
