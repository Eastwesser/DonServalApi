from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from api.core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )

    # Function to provide async DB sessions as a dependency in FastAPI routes.
    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
