from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_async_session, Database
from users.models import User
from sqlalchemy import update
from auth.routers import current_active_user


email_router = APIRouter(
    prefix="/email_verif",
    tags=["Роутер для верификации почты пользователя с лк"]
)


@email_router.post('/verif')
async def verify_email(
    verif_token: str,
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
