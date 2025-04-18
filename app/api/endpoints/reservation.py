# app/api/endpoints/reservation.py
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.models import User

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
        user: User = Depends(current_user),
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
        user=user,
        session=session,
    )
    return reservation


@router.get(
    '/',
    response_model=list[ReservationDB],
    dependencies=[Depends(current_superuser)],
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
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> ReservationDB:
    db_obj = await check_reservation_before_edit(
        user=user, reservation_id=reservation_id, session=session
    )
    return await reservation_crud.remove(db_obj=db_obj, session=session)


@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    # Проверяем, что такой объект бронирования вообще существует.
    reservation = await check_reservation_before_edit(
        user=user, reservation_id=reservation_id, session=session
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


@router.get(
    '/my_reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'}
)
async def get_my_reservations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> list[ReservationDB]:
    return await reservation_crud.get_by_user(user_id=user.id, session=session)
