from auth.routers import current_active_verified_user 
from fastapi import Depends, APIRouter, Path, Form
from typing import Annotated, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_async_session, Database
from enums import Mark
from .schemas import ReviewRead
from .models import Review


reviews_router = APIRouter(
    prefix="/reviews",
    tags=["Роутер отзывов пользователей"]
)

@reviews_router.get("/list")
async def reviews_list(
    async_session: AsyncSession = Depends(get_async_session)
) -> List[ReviewRead]:
    db = Database(session=async_session)
    reviews = await db.review.get_by_where(
        Review.moderated == True
    )
    return reviews

@reviews_router.get("/{review_id}")
async def review_id(
    review_id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session),
) -> ReviewRead:
    db = Database(session=async_session)
    review = await db.review.get(ident=review_id)
    return review

@reviews_router.post("review_form")
async def review_form(
    text: Optional[str] = Form(max_length=250),
    rating: Mark = Form(),
    async_session: AsyncSession = Depends(get_async_session)
) -> str:
    db = Database(session=async_session)

    review = await db.review.new(
        text=text,
        rating=rating,
        moderated=False
    )
    db.session.add(review)
    await db.session.flush()
    return "Благодарим за отзыв"
