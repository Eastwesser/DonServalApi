from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.core.db_helper import db_helper
from api.core.models import Base
from api.donuts.views.views import router as donuts_router


# Define a context manager to manage the lifespan of the application.
# It ensures that the database tables are created when the app starts.
@asynccontextmanager
async def lifespan(_: FastAPI):
    async with db_helper.engine.begin() as conn:
        # Create all database tables defined in the models
        await conn.run_sync(Base.metadata.create_all)
    yield


# Instantiate the FastAPI app with metadata like title and description.
# The 'lifespan' argument binds the above context manager to the app's lifecycle.
app = FastAPI(
    title="DonServal API",
    description="Serval Donut API for the donut shop",
    version="1.0.0",
    lifespan=lifespan,
)

# Include the donut-specific routes from the 'donuts_router'.
# All endpoints related to donuts will be prefixed with '/donuts'.
app.include_router(
    donuts_router,
    prefix="/donuts",
)

# This block runs the app with Uvicorn when the script is executed directly.
if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # Tells Uvicorn to run the 'app' instance defined above.
        host="0.0.0.0",  # Binds the server to all available IP addresses.
        port=8000,  # Specifies the port on which the app will run.
        reload=True,  # Enables auto-reloading when code changes (useful for development).
    )
