# app/api/routers.py
from fastapi import APIRouter

from .endpoints import endpoints_router, reservation_router, meeting_room_router, users_router
main_router = APIRouter()

main_router.include_router(
    meeting_room_router, tags=["meeting_room"], prefix='/meeting_room'
)
main_router.include_router(
    reservation_router, prefix='/reservations', tags=['Reservations']
)
main_router.include_router(endpoints_router, tags=["Синхронные"])

main_router.include_router(users_router)
