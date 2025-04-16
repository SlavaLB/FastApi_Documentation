# app/core/config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    ...

    class Config:
        env_file = '.env'
