
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # Database configuration
    DB_CONNECTION: str

    # JWT configuration
    SECRET_KEY: str
    ALGORITHM: str
    EXP_TIME: int

    # Email configuration
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str


settings = Settings()
