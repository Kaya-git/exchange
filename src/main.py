from fastapi import FastAPI
from config import conf
from exchange.forms import forms_router


app = FastAPI(
    title="Exchange"
)

app.include_router(forms_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", log_level=conf.logging_level, reload=True)
