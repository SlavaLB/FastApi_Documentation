# app/schemas/meeting_room.py

from typing import Optional

from pydantic import BaseModel, Field, validator

from app.schemas.reservation import ReservationDB, ReservationDBALL


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomUpdate(MeetingRoomBase):
    pass

    @validator('name')
    def validate_name(cls, value):
        if not value:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


class MeetingRoomDB(MeetingRoomCreate):
    id: int

    class Config:
        orm_mode = True


class MeetingRoomDBAll(MeetingRoomCreate):
    id: int
    reservations: list[ReservationDBALL]

    class Config:
        orm_mode = True
