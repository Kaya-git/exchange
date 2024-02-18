import logging
import uuid

from fastapi import BackgroundTasks, Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncSession

from admin import (ContactAdmin, CurrencyAdmin, FAQAdmin, OrderAdmin,
                   PaymentOptionAdmin, PendingAdminAdmin, ReviewAdmin,
                   ServicePaymentOptionAdmin, UserAdmin)
from auth.auth import auth_backend
from auth.routers import fastapi_users
from auth.shemas import UserCreate, UserRead
from background_tasks.handlers import cache_rates
from config import conf
from contacts.routers import contact_router
from currencies.routers import currency_router
from database.db import engine, get_async_session
from exchange.routers import exchange_router
from faq.routers import faq_router
from google_recaptcha.routers import recaptcha_router
from mail_verif.routers import email_router
from orders.routers import orders_router
from redis_ttl.routers import redis_router
from reviews.routers import reviews_router
from users.routers import lk_router
from where_am_i.routers import where_am_i_router

app = FastAPI(
    title="Exchange"
)

LOGGER = logging.getLogger(__name__)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "https://localhost",
    "https://localhost:8080",
    "https://localhost:8000",
    "http://89.105.198.9",
    "http://89.105.198.9:8080",
    "http://89.105.198.9:8000",
    "https://89.105.198.9",
    "https://89.105.198.9:8080",
    "https://89.105.198.9:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET", "POST",
        "OPTIONS", "DELETE",
        "PATCH", "PUT"
    ],
    allow_headers=[
        "Content-Type", "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization"],
)


admin = Admin(
    app=app,
    engine=engine,
    # authentication_backend=authentication_backend
)

admin.add_view(PendingAdminAdmin)
admin.add_view(UserAdmin)
admin.add_view(ServicePaymentOptionAdmin)
admin.add_view(ReviewAdmin)
admin.add_view(CurrencyAdmin)
admin.add_view(PaymentOptionAdmin)
admin.add_view(OrderAdmin)
admin.add_view(ContactAdmin)
admin.add_view(FAQAdmin)


@app.get("/api/uuid")
async def root(
    response: Response,
    background_tasks: BackgroundTasks,
    async_session: AsyncSession = Depends(get_async_session),

):
    """Устанавливаем печеньки на пользователя"""
    cookies_uuid = uuid.uuid4()
    response.set_cookie(key="user_uuid", value=cookies_uuid)
    background_tasks.add_task(cache_rates)
    return cookies_uuid

app.include_router(recaptcha_router)
app.include_router(email_router)
app.include_router(redis_router)
app.include_router(lk_router)
app.include_router(where_am_i_router)
app.include_router(contact_router)
app.include_router(faq_router)
app.include_router(currency_router)
app.include_router(orders_router)
app.include_router(exchange_router)
app.include_router(reviews_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api/auth",
    tags=["auth"],
)


@app.on_event("startup")
async def startup():

    redis = aioredis.from_url(
        f"redis://{conf.redis.host}:{conf.redis.port}",
        encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    LOGGER.info("--- Start up App ---")


@app.on_event
async def shutdown():
    LOGGER.info("--- Shudown App ---")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app)
