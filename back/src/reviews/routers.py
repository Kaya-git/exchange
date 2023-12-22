from typing import TYPE_CHECKING, Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from auth.routers import current_active_verified_user
from database.db import Database, get_async_session

from enums.models import ReqAction
from fastapi_cache.decorator import cache
from .models import Review
from .schemas import ReviewDTO, ReviewCreateDTO
if TYPE_CHECKING:
    from users.models import User


reviews_router = APIRouter(
    prefix="/api/reviews",
    tags=["Роутер отзывов пользователей"]
)


@reviews_router.get("/list", response_model=List[ReviewDTO])
@cache(expire=300)
async def reviews_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    reviews = await db.review.get_by_where(
        Review.moderated is True
    )
    return reviews


@reviews_router.get("/{review_id}", response_model=ReviewDTO)
@cache(expire=300)
async def review_id(
    review_id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session),
):
    db = Database(session=async_session)
    review = await db.review.get(ident=review_id)
    return review


@reviews_router.post("/review_form")
async def review_form(
    review_create: ReviewCreateDTO,
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_verified_user)
) -> str:
    db = Database(session=async_session)

    review = await db.review.new(
        user_id=user.id,
        text=review_create.text,
        rating=review_create.rating,
        moderated=False
    )
    db.session.add(review)
    await db.session.flush()

    new_pending_review = await db.pending_admin.new(
        review_id=review.id,
        req_act=ReqAction.VerifyReview
    )
    db.session.add(new_pending_review)
    await db.session.flush()

    await db.session.commit()
    return "Благодарим за отзыв"
