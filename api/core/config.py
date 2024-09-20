from pydantic import ConfigDict
from pydantic_settings import BaseSettings


# Settings class for configuring the application.
class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str
    db_echo: bool = False

    model_config = ConfigDict(
        env_file=".env",  # Read settings from the environment file.
        extra="allow",
    )


# Create an instance of the Settings class to access configuration.
settings = Settings()
