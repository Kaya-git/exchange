from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_async_session, Database
from users.models import User
from sqlalchemy import update

email_router = APIRouter(
    prefix="email_verif",
    tags=["Роутер для верификации почты пользователя с лк"]
)


@email_router.post('/verif')
async def verify_email(
    verif_token: str,
    session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=session)
    user = db.user.get_by_where(
        User.verification_token == verif_token
    )

    if user:
        statement = update(
            User
        ).where(
            User.verification_token == verif_token
        ).values(
            is_verified=True
        )
        await db.session.execute(statement)
        await db.session.commit()
        return {
            "verified": True
        }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Такого ключа не существует"
    )
