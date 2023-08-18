from fastapi import APIRouter
from .constants import EMAIL_QUEUE

exhange_router = APIRouter(
    prefix="/exchange_router",
    tags=["exchange_router"]
)


@exhange_router.get("/confirm_cc")
async def confirm_cc():
    email = await EMAIL_QUEUE.get()
    return f"{email}"
