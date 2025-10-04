from enum import StrEnum

from dotenv import find_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8080
    DEV: bool = True

    # Database Configuration
    DATABASE_TYPE: DatabaseType = DatabaseType.POSTGRES

    # PostgreSQL Configuration
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_APPLICATION_NAME: str

    POSTGRES_MIN_CONNECTIONS_PER_POOL: int = 1
    POSTGRES_MAX_CONNECTIONS_PER_POOL: int = 1

    # MongoDB Configuration
    MONGO_URI: str
    MONGO_USER: str
    MONGO_PASSWORD: SecretStr
    MONGO_DB_NAME: str
    MONGO_AUTH_SOURCE: str
    MONGO_STATE_CHECKPOINT_COLLECTION: str = "state_checkpoints"
    MONGO_STATE_WRITES_COLLECTION: str = "state_writes"
    MONGO_STATE_STORE_COLLECTION: str = "state_store"

    @property
    def postgres_dsn(self) -> str:
        pwd = self.POSTGRES_PASSWORD.get_secret_value()
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{pwd}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def mongo_dsn(self) -> str:
        pwd = self.MONGO_PASSWORD.get_secret_value()
        return (
            f"mongodb://{self.MONGO_USER}:{pwd}@{self.MONGO_URI.split('//')[-1]}"
            f"/{self.MONGO_DB_NAME}?authSource={self.MONGO_AUTH_SOURCE}"
        )


settings = Settings()  # type: ignore
