from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str
    db_echo: bool = False

    model_config = ConfigDict(
        env_file=".env",
        extra="allow",
    )


settings = Settings()
