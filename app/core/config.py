# core/config.py
from typing import Optional

from pydantic import BaseSettings, Field, EmailStr
from datetime import date


class Settings(BaseSettings):
    app_title: str = Field(..., env='APP_TITLE')
    app_author: str = Field(..., env='APP_AUTHOR')
    author_pass: str = Field(..., env='AUTHOR_PASS')
    deadline_date: date = Field(..., env='DEADLINE_DATE')
    # path: Path = Field(..., env='PATH')
    secret: str = Field('SECRET', env='SECRET_KEY')
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    database_url: str

    class Config:
        env_file = '.env'
        # env_prefix = 'MYAPP_'  # используем префикс по умолчанию, можно не задавать, если в Field указываешь env


settings = Settings()
print(settings.secret)