# app/api/meeting_room.py

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.reservation import reservation_crud

from app.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate, MeetingRoomDBAll
)

from app.crud.meeting_room import meeting_room_crud
from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.schemas.reservation import ReservationDB

from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=MeetingRoomDB,
    # Исключение пустых полей из ответа
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        session: AsyncSession = Depends(get_async_session),
):
    # Выносим проверку дубликата имени в отдельную корутину.
    # Если такое имя уже существует, то будет вызвана ошибка HTTPException
    # и обработка запроса остановится.
    await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[MeetingRoomDB]
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session)
) -> list[MeetingRoomDB]:
    return await meeting_room_crud.get_multi(session)


@router.get(
    '/all_info',
    response_model_exclude_none=True,
    response_model=list[MeetingRoomDBAll]
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session)
) -> list[MeetingRoomDBAll]:
    return await meeting_room_crud.get_all(session)


@router.patch(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        meeting_room_id: int,
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    # Выносим повторяющийся код в отдельную корутину.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> MeetingRoomDB:

    meeting_room = await check_meeting_room_exists(meeting_room_id, session)

    result = await meeting_room_crud.remove(meeting_room, session)
    print(result)
    return result


@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'}
)
async def get_reservations_for_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> list[ReservationDB]:
    await check_meeting_room_exists(
        meeting_room_id=meeting_room_id, session=session
    )
    return await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id, session=session
    )
