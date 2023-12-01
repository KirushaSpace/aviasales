import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    DATABASE_URL: str

    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


settings = Settings()