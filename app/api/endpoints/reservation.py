# app/api/endpoints/reservation.py
from typing import Union

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.reservation import reservation_crud

from app.core.db import get_async_session

from app.schemas.reservation import ReservationDB, ReservationCreate, \
    ReservationUpdate

from app.api.validators import check_meeting_room_exists, \
    check_reservation_intersections, check_reservation_before_edit

from app.crud.reservation import reservation_crud

router = APIRouter()


@router.post(
    '/',
    response_model=ReservationDB
)
async def create_reservation(
        reservation: ReservationCreate,
        session: AsyncSession = Depends(get_async_session),
) -> ReservationDB:
    await check_meeting_room_exists(
        meeting_room_id=reservation.meetingroom_id, session=session
    )
    await check_reservation_intersections(
        **reservation.dict(),
        session=session,
    )
    reservation = await reservation_crud.create(
        obj_in=reservation,
        session=session,
    )
    return reservation


@router.get(
    '/',
    response_model=list[ReservationDB],
)
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session),
) -> list[ReservationDB]:
    return await reservation_crud.get_multi(session=session)


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB,
)
async def get_all_reservations(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> ReservationDB:
    db_obj = await check_reservation_before_edit(
        reservation_id=reservation_id, session=session
    )
    return await reservation_crud.remove(db_obj=db_obj, session=session)


@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    # Проверяем, что такой объект бронирования вообще существует.
    reservation = await check_reservation_before_edit(
        reservation_id, session
    )
    # Проверяем, что нет пересечений с другими бронированиями.
    await check_reservation_intersections(
        # Новое время бронирования, распакованное на ключевые аргументы.
        **obj_in.dict(),
        # id обновляемого объекта бронирования,
        reservation_id=reservation_id,
        # id переговорки.
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        # На обновление передаем объект класса ReservationUpdate, как и требуется.
        obj_in=obj_in,
        session=session,
    )
    return reservation

