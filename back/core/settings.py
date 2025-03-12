from typing import Any, Optional

import pydantic
import pydantic.class_validators
import pydantic_settings


class DatabaseSettings(pydantic_settings.BaseSettings):
    DB_PORT: int = pydantic.Field(3306)
    REDIS_PORT: int = pydantic.Field(6379)
    DB_NAME: str = pydantic.Field("db")
    DB_USER: str = pydantic.Field("user")
    DB_HOST: str = pydantic.Field("localhost")
    DB_PASSWORD: str = pydantic.Field("password")
    REDIS_PORT: int = pydantic.Field(6379)

    DB_URL: Optional[str] = None

    @pydantic.field_validator("DB_URL", mode="before")
    def assemble_db_connection(
        cls, v: str, info: pydantic.FieldValidationInfo
    ) -> pydantic.AnyUrl:
        values = info.data
        if isinstance(v, str):
            return v
        url = pydantic.AnyUrl.build(
            scheme="mysql+pymysql",
            username=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=values.get("DB_NAME", ""),
        )
        return str(url)


class Settings(DatabaseSettings):
    # for dotenv
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )
    DEBUG: bool = False


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
