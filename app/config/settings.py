from dotenv import find_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr



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