import os

from pydantic import Field
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    """ Base class for settings """

    class Config:
        env_file = f".{os.getenv('ENVIRONMENT', 'dev')}.env"   # path to Environment
        env_file_encoding = 'utf-8'


# noinspection PyArgumentList
class Tokens(_Settings):
    """ Class for tokens """
    TOKEN_1: str = Field(default="token1", env="TOKEN1")
    TOKEN_2: str = Field(default="token2", env="TOKEN2")
    TOKEN_3: str = Field(default="token3", env="TOKEN3")


# noinspection PyArgumentList
class SecuritySettings(_Settings):
    """ Class for security settings """
    SECURITY: bool = Field(default=False, env="SECURITY")
    ADMINS_IDS: list[int] = Field(default=[], env='ADMINS_IDS')

    class Config(_Settings.Config):
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> list[str | int]:
            if field_name == 'ADMINS_IDS':
                return [int(ID) for ID in raw_val.split(',') if ID]
            return cls.json_loads(raw_val)  # noqa


# noinspection PyArgumentList
class RabbitMQSettings(_Settings):
    """ Class for RabbitMQ settings """
    RABBITMQ_HOST: str = Field(default="localhost", env="RABBITMQ_HOST")
    RABBITMQ_PORT: int = Field(default=5672, env="RABBITMQ_PORT")
    RABBITMQ_USER: str = Field(default="guest", env="RABBITMQ_USER")
    RABBITMQ_PASSWORD: str = Field(default="guest", env="RABBITMQ_PASSWORD")

    @property
    def rabbitmq_url(self):
        return f"pyamqp://{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"

    @property
    def rabbitmq_url_with_user(self):
        return f"pyamqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"


# noinspection PyArgumentList
class RedisSettings(_Settings):
    """ Class for Redis settings """
    REDIS_ADDRESS: str = Field(default="localhost", env="REDIS_ADDRESS")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_USER: str = Field(default="guest", env="REDIS_USER")
    REDIS_PASSWORD: str = Field(default="guest", env="REDIS_PASSWORD")
    REDIS_DB_NUMBER: int = Field(default=0, env="REDIS_DB_NUMBER")

    DROP_CACHE: bool = Field(default=False, env="DROP_CACHE")

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_ADDRESS}/{self.REDIS_DB_NUMBER}"

    @property
    def redis_url_with_user(self):
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_ADDRESS}:{self.REDIS_PORT}"


# noinspection PyArgumentList
class MongoSettings(_Settings):
    """ Class for Mongo DB settings """
    MONGO_USERNAME: str = Field(default="user", env="MONGO_USERNAME")
    MONGO_PASSWORD: str = Field(default="password", env="MONGO_PASSWORD")
    MONGO_HOST: str = Field(default="localhost", env="MONGO_HOST")
    MONGO_OPTIONS: str = Field(default="authSource=admin", env="MONGO_OPTIONS")
    MONGO_DB: str = Field(default="giveaway_bot", env="MONGO_DB")

    DROP_DB: bool = Field(default=False, env="DROP_DB")

    @property
    def mongo_url(self):
        return f"mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}/?{self.MONGO_OPTIONS}"


# noinspection PyArgumentList
class SQLSettings(_Settings):
    """ Class for SQL DB settings """
    DB_ENGINE: str = Field(default="postgresql", env='DB_ENGINE')
    DB_USER: str = Field(default="postgres", env='DB_USER')
    DB_PASSWORD: str = Field(default="postgres", env='DB_PASSWORD')
    DB_ADDRESS: str = Field(default="localhost", env='DB_ADDRESS')
    DB_PORT: int = Field(default=5432, env='DB_PORT')
    DB_NAME: str = Field(default="new_project_db", env='DB_NAME')

    DROP_DB: bool = Field(default=False, env="DROP_DB")

    @property
    def sync_database_url(self):
        return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_ADDRESS}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def async_database_url(self):
        return f"{self.DB_ENGINE}+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_ADDRESS}:{self.DB_PORT}/{self.DB_NAME}"


# noinspection PyArgumentList
class WebSettings(_Settings):
    USE_WEBHOOK: bool = Field(default=False, env="USE_WEBHOOK")
    WEBHOOK_HOST: str = Field(default="", env="WEBHOOK_HOST")
    INNER_WEBHOOK_PORT: int = Field(default=8888, env="INNER_WEBHOOK_PORT")
    TELEGRAM_WEBHOOK_PORT: int = Field(default=8443, env="TELEGRAM_WEBHOOK_PORT")
    WEBHOOK_PATH: str = Field(default="webhook", env="WEBHOOK_PATH")

    @property
    def webhook_url(self):
        return f"https://{self.WEBHOOK_HOST}"


# noinspection PyArgumentList
class Settings(SecuritySettings, RedisSettings, MongoSettings, RabbitMQSettings, WebSettings):
    """ Use this class for other settings """
    LOG_DIR: str = Field(default=".logs")

    # Starting settings
    DEBUG: bool = Field(default=False, env="DEBUG")


project_settings = Settings()

__all__ = [
    "project_settings",
    "Tokens",
    "SecuritySettings",
    "RabbitMQSettings",
    "RedisSettings",
    "MongoSettings",
    "SQLSettings",
    "WebSettings",
]
