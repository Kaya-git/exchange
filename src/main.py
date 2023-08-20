from fastapi import FastAPI, Response
from config import conf
from exchange import forms_router, exhange_router
from sqladmin import Admin
from database.db import create_async_engine
from admin import (UserAdmin,
                   PendingAdmin,
                   CommissionsAdmin,
                   OrdersHistoryAdmin
)
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from auth.manager import get_user_manager
from database.models import User
import uuid

async_engine = create_async_engine(conf.db.build_connection_str())


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
app = FastAPI(
    title="Exchange"
)
admin = Admin(
    app=app,
    engine=async_engine
)

admin.add_view(UserAdmin)
admin.add_view(PendingAdmin)
admin.add_view(CommissionsAdmin)
admin.add_view(OrdersHistoryAdmin)


@app.get("/")
async def root(response: Response):
    user_id = uuid.uuid4()
    response.set_cookie(key="user_id", value=user_id)
    return "установили куки"

app.include_router(forms_router)
app.include_router(exhange_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
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

    uvicorn.run("main:app", log_level=conf.logging_level, reload=True)
