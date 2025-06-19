import os
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()
# abs_path_env = os.path.abspath("../.env")

secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')

class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD']

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
TEST_DATABASE_URL = f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
