# app/schemas/meeting_room.py
from datetime import datetime

from pydantic import BaseModel, root_validator, validator


class ReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime


class ReservationUpdate(ReservationBase):
    pass

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value: datetime) -> datetime:
        if value <= datetime.now():
            raise ValueError('Время бронирования не может быть раньше текущего времени.')
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return values


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int

    class Config:
        orm_mode = True
