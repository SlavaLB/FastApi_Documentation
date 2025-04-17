from datetime import datetime

from fastapi import HTTPException

from sqlalchemy import select, and_

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.meeting_room import MeetingRoomDB
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.schemas.reservation import ReservationDB


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )


async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession,
) -> MeetingRoomDB:
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена'
        )
    return meeting_room


async def check_reservation_intersections(
        **kwargs
) -> None:
    result = await reservation_crud.get_reservations_at_the_same_time(
        **kwargs
    )
    if result:
        raise HTTPException(
            status_code=422,
            detail='На это время переговорки заняты'
        )


async def check_reservation_before_edit(reservation_id, session: AsyncSession) -> ReservationDB:
    result = await reservation_crud.get(obj_id=reservation_id, session=session)
    if not result:
        raise HTTPException(
            status_code=404,
            detail='Бронирование не найдено'
        )
    return result
