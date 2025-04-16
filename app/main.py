from fastapi import FastAPI

from app.api.endpoints import router

from app.core.config import settings

app = FastAPI(title=settings.app_title, description=settings.app_author)

app.include_router(router)
