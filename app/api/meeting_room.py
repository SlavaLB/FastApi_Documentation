# app/api/meeting_room.py

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.meeting_room import create_meeting_room, get_room_id_by_name, read_all_rooms_from_db
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB

router = APIRouter(prefix='/meeting_room')


@router.post(
    '/',
    response_model=MeetingRoomDB,
    # Исключение пустых полей из ответа
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        session: AsyncSession = Depends(get_async_session),
):
    # Вызываем функцию проверки уникальности поля name:
    room_id = await get_room_id_by_name(meeting_room.name, session)
    # Если такой объект уже есть в базе - вызываем ошибку:
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )
    new_room = await create_meeting_room(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[MeetingRoomDB]
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session)
) -> list[MeetingRoomDB]:
    return await read_all_rooms_from_db(session)
