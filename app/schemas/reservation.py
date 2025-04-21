# app/schemas/meeting_room.py
from datetime import datetime, timedelta

from typing import Optional

from pydantic import BaseModel, root_validator, validator, Field, Extra

from app.schemas.user import UserRead

FROM_TIME = (datetime.now()+timedelta(minutes=3)).isoformat(timespec='minutes')
TO_TIME = (datetime.now()+timedelta(minutes=20)).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid


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
    meetingroom_id: int = Field(..., example=1)


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True


class ReservationDBALL(ReservationBase):
    id: int
    # meetingroom_id: int
    user: Optional[UserRead]

    class Config:
        orm_mode = True
