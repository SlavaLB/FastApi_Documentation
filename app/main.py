from fastapi import FastAPI

from app.api.endpoints import router as api_router
from app.api.meeting_room import router as meeting_room

from app.core.config import settings

app = FastAPI(title=settings.app_title, description=settings.app_author)

app.include_router(api_router, tags=["Синхронные"])
app.include_router(meeting_room, tags=["Асинхронные"])
