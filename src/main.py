from fastapi import FastAPI, Depends
from config import conf
from exchange import forms_router, exhange_router
from sqladmin import Admin
from database.db import create_async_engine
from admin import UserAdmin

app = FastAPI(
    title="Exchange"
)
admin = Admin(
    app=app,
    engine=Depends(create_async_engine(conf.db.build_connection_str()))
)

admin.add_view(UserAdmin)


@app.get("/")
async def exchange():
    return "Первая страница с формами на обмен"

app.include_router(forms_router)
app.include_router(exhange_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", log_level=conf.logging_level, reload=True)
