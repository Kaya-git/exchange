from fastapi import APIRouter


exhange_router = APIRouter(
    prefix="/exchange_router",
    tags=["exchange_router"]
)


@exhange_router.get("/confirm_cc")
async def confirm_cc():
    print("SUCCESS")
