from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str
    db_echo: bool = False

    class Config:
        env_file = ".env"
        extra = Extra.allow


settings = Settings()
