from fastapi import FastAPI, Response, Depends
from database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi.responses import RedirectResponse
from config import conf
from exchange.routers import exchange_router
from sqladmin import Admin
from database.db import engine
from admin import (
    UserAdmin,
    ServicePaymentOptionAdmin,
    CurrencyAdmin,
    PaymentOptionAdmin,
    ReviewAdmin,
    OrderAdmin,
    ContactAdmin,
    FAQAdmin,
    PendingAdminAdmin
)
from auth.auth import auth_backend
from auth.shemas import UserRead, UserCreate
from auth.routers import fastapi_users
from currencies.routers import currency_router
from admin.auth_back import authentication_backend
from reviews.routers import reviews_router
from orders.routers import orders_router
from contacts.routers import contact_router
from faq.routers import faq_router
import uuid
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse


app = FastAPI(
    title="Exchange"
)

origins = [
    "http://localhost:8080",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
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


@app.get("/")
async def root(
    response: Response,
    async_session: AsyncSession = Depends(get_async_session),
):

    """Устанавливаем печеньки на пользователя"""
    cookies_uuid = uuid.uuid4()
    response.set_cookie(key="user_uuid", value=cookies_uuid)

app.include_router(contact_router)
app.include_router(faq_router)
app.include_router(currency_router)
app.include_router(orders_router)
app.include_router(exchange_router)
app.include_router(reviews_router)
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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
