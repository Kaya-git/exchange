from fastapi import FastAPI
from config import conf

app = FastAPI(
    title="Exchange"
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", log_level=conf.logging_level, reload=True)
