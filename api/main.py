from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.core.db_helper import db_helper
from api.core.models import Base
from api.donuts.views.views import router as donuts_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="DonServal API",
    description="Serval Donut API for the donut shop",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    donuts_router,
    prefix="/donuts",
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
