# app/crud/meeting_room.py

from typing import Optional

# Добавляем импорт функции select.
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.meeting_room import MeetingRoom

from .base import CRUDBase
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate, \
    MeetingRoomDBAll, MeetingRoomDB
from ..models import Reservation


class CRUDMeetingRoom(CRUDBase[
    MeetingRoom,
    MeetingRoomCreate,
    MeetingRoomUpdate,
]):
    async def get_room_id_by_name(
            self,
            room_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_room_id = await session.execute(
            select(self.model.id).where(
                self.model.name == room_name
            )
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id

    async def get_all(self, session: AsyncSession) -> list[MeetingRoomDBAll]:
        result = await session.execute(
            select(self.model).options(
                joinedload(MeetingRoom.reservations).joinedload(
                    Reservation.user)
            )
        )
        return result.unique().scalars().all()


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)

