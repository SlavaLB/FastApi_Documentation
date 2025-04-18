# app/crud/reservation.py
from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate, \
    ReservationDB


class CRUDReservation(CRUDBase[Reservation, ReservationCreate, ReservationUpdate]):
    @staticmethod
    async def get_reservations_at_the_same_time(
            # Добавляем звёздочку, чтобы обозначить, что все дальнейшие параметры
            # должны передаваться по ключу. Это позволит располагать
            # параметры со значением по умолчанию перед параметрами без таких значений.
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            # Добавляем новый опциональный параметр - id объекта бронирования.
            reservation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> list[Reservation]:
        # Выносим уже существующий запрос в отдельное выражение.
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        # Если передан id бронирования...
        if reservation_id is not None:
            # ... то к выражению нужно добавить новое условие.
            select_stmt = select_stmt.where(
                # id искомых объектов не равны id обновляемого объекта.
                Reservation.id != reservation_id
            )
        # Выполняем запрос.
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    @staticmethod
    async def get_future_reservations_for_room(
            room_id: int, session: AsyncSession
    ) -> list[ReservationDB]:
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == room_id,
            and_(
                Reservation.to_reserve > datetime.now(),
            )
        )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    @staticmethod
    async def get_by_user(user_id: int, session: AsyncSession) -> list[ReservationDB]:
        select_stmt = select(Reservation).where(Reservation.user_id == user_id)
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
