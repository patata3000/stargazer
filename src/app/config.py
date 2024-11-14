import logging

from pydantic import field_validator, PostgresDsn, ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Hold the configuration of the entire app."""

    API_V1_STR: str = "/api/v1"
    """Route prefix for v1 API."""

    PROJECT_NAME: str = "stargazer"
    """Name of the project. Used as title for fastapi App."""

    CLIENT_ID: str = "1056082"
    """The id of the Github App used to authenticate."""
    PRIVATE_KEY_PATH: str = "./private_key.pem"
    """Path to the private key."""
    PRIVATE_KEY: str = ""
    """The private key used to authenticate as a Github App.

    This has priority over the `PRIVATE_KEY_PATH` config."""

    @field_validator("PRIVATE_KEY", mode="before")
    @classmethod
    def extract_private_key(cls, v: str, info: ValidationInfo) -> str:
        if v and isinstance(v, str):
            return v
        pk_path = info.data.get("PRIVATE_KEY_PATH")
        assert isinstance(pk_path, str)
        with open(pk_path) as file:
            return file.read()

    PER_PAGE: int = 100
    """When fetching data using Github api, this is the number of item
    fetched by one call.

    From Github doc, max is 100.
    """
    NB_CONCURRENT_PROCESSES: int = 4
    """When fetching data using Github api, this is the number of concurrent
    threads.

    This can be tweaked based on the machine. A number too high will lead to
    errors coming from Github servers caused by rate limit.
    """

    LOGGING_LEVEL: int = logging.DEBUG
    """Global logging level."""

    # ECHO_SQL_QUERIES: bool = False

    # DB_HOST: str
    # DB_PORT: str
    # DB_USER: str
    # DB_PASSWORD: str
    # DB_NAME: str

    # SQLALCHEMY_DATABASE_URI: PostgresDsn | str = ""


settings = Settings()  # pyright: ignore

logging.basicConfig(level=settings.LOGGING_LEVEL)
