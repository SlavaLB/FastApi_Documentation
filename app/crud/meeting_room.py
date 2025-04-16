# app/crud/meeting_room.py
from fastapi.encoders import jsonable_encoder

from typing import Optional, Union

# Добавляем импорт функции select.
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate, \
    MeetingRoomDB


async def create_meeting_room(
        new_room: MeetingRoomCreate,
        session: AsyncSession
) -> MeetingRoom:

    new_room_data = new_room.dict()
    db_room = MeetingRoom(**new_room_data)
    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)
    return db_room


async def get_room_id_by_name(
        room_name: str,
        session: AsyncSession
) -> Optional[int]:

    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        )
    )
    db_room_id = db_room_id.scalars().first()
    return db_room_id


async def read_all_rooms_from_db(
        session: AsyncSession
) -> list[MeetingRoom]:
    result = await session.execute(select(MeetingRoom))
    return result.scalars().all()


async def get_meeting_room_by_id(
        meeting_room_id: int,
        session: AsyncSession
) -> Union[MeetingRoom, None]:
    result = await session.execute(select(MeetingRoom).where(MeetingRoom.id == meeting_room_id))
    return result.scalars().first()
    # return await session.get(MeetingRoom, meeting_room_id) Тот же результат


async def update_meeting_room(
        db_room: MeetingRoomDB,  # Объект из БД для обновления.
        room_in: MeetingRoomUpdate,  # Объект из запроса.
        session: AsyncSession,
) -> MeetingRoomDB:
    obj_data = jsonable_encoder(db_room)  # Представляем объект из БД в виде словаря.
    # Конвертируем объект с данными из запроса в словарь,
    # исключаем неустановленные пользователем поля.
    update_data = room_in.dict(exclude_unset=True)

    # Перебираем все ключи словаря, сформированного из БД-объекта.
    for field in obj_data:
        # Если конкретное поле есть в словаре с данными из запроса, то...
        if field in update_data:
            # ...устанавливаем объекту БД новое значение атрибута.
            setattr(db_room, field, update_data[field])
    # Добавляем обновленный объект в сессию.
    session.add(db_room)
    # Фиксируем изменения.
    await session.commit()
    # Обновляем объект из БД.
    await session.refresh(db_room)
    return db_room


async def delete_room(meeting_room: MeetingRoomDB, session: AsyncSession):
    await session.delete(meeting_room)
    await session.commit()
    return meeting_room
