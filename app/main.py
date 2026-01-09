from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db, seed_db
from .router import router
from .tasks import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_db()
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
