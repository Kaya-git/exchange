from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.routers import current_active_user
from database.db import Database, get_async_session
from users.models import User

email_router = APIRouter(
    prefix="/api/email_verif",
    tags=["Роутер для верификации почты пользователя с лк"]
)


@email_router.post('/verif')
async def verify_email(
    verif_token: str | None = Form(),
    session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_user)
):
    db = Database(session=session)

    print(user.verification_token)
    if verif_token == str(user.verification_token):
        await db.user.update_verification(user.id)
        return {
            "verified": True
        }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Такого ключа не существует"
    )
