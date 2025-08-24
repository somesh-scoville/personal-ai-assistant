from dotenv import find_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from enum import StrEnum

class DatabaseType(StrEnum):
    POSTGRES = "postgres"
    MONGO = "mongo"

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        validate_default=False,
    )


    # SERVICE_HOST : str ="0.0.0.0"
    # SERVICE_PORT : int = 8080
    # DEV : bool = True

    SERVICE_HOST : str | None = None
    SERVICE_PORT : int | None = None
    DEV : bool = True


    # Database Configuration
    DATABASE_TYPE: DatabaseType = (
        DatabaseType.POSTGRES
    )

    # PostgreSQL Configuration
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: SecretStr | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: int | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_APPLICATION_NAME: str = "personal-ai-assistant"
    POSTGRES_MIN_CONNECTIONS_PER_POOL: int = 1
    POSTGRES_MAX_CONNECTIONS_PER_POOL: int = 1


    # MongoDB Configuration
    MONGO_URI: str | None = None
    MONGO_USER: str | None = None
    MONGO_PASSWORD: SecretStr | None = None
    MONGO_DB_NAME: str | None = None
    MONGO_AUTH_SOURCE: str | None = None
    MONGO_STATE_CHECKPOINT_COLLECTION: str | None = None
    MONGO_STATE_WRITES_COLLECTION: str | None = None
    MONGO_STATE_STORE_COLLECTION: str | None = None




settings = Settings()