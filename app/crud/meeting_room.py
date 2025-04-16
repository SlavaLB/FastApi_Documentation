# app/crud/meeting_room.py

from typing import Optional

# Добавляем импорт функции select.
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.meeting_room import MeetingRoom

from .base import CRUDBase
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


class CRUDMeetingRoom(CRUDBase[
    MeetingRoom,
    MeetingRoomCreate,
    MeetingRoomUpdate
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


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)

