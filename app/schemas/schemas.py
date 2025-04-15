import re
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, validator, root_validator


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


class User(BaseModel):
    name: str
    age: int
    email: str


class Person(BaseModel):
    name: str = Field(..., max_length=20, description='Можно вводить в любом регистре', title='Полное имя')
    surname: Union[str, list[str]] = Field(..., max_length=50)
    age: Optional[int] = Field(None, gt=4, le=99)
    is_staff: bool = Field(False, alias='is-staff')
    education_level: Optional[EducationLevel]

    class Config:
        title = 'Класс для приветствия'
        min_anystr_length = 2
        schema_extra = {
            'examples': {
                'single_surname': {
                    'summary': 'Одна фамилия',
                    'description': 'Одиночная фамилия передается строкой',
                    'value': {
                       'name': 'Taras',
                       'surname': 'Belov',
                       'age': 20,
                       'is_staff': False,
                       'education_level': 'Среднее образование'
                    }
                },
                'multiple_surnames': {
                    'summary': 'Несколько фамилий',
                    'description': 'Несколько фамилий передаются списком',
                    'value': {
                       'name': 'Eduardo',
                       'surname': ['Santos', 'Tavares'],
                       'age': 20,
                       'is_staff': False,
                       'education_level': 'Высшее образование'
                    }
                },
                'invalid': {
                    'summary': 'Некорректный запрос',
                    'description': 'Возраст передается только целым числом',
                    'value': {
                        'name': 'Eduardo',
                        'surname': ['Santos', 'Tavares'],
                        'age': 'forever young',
                        'is_staff': False,
                        'education_level': 'Среднее специальное образование'
                    }
                }
            }
        }

    @validator('name')
    def name_cant_be_numeric(cls, value: str):
        if re.search(r'\d', value):
            raise ValueError('Имя не может быть числом')
        return value

    @root_validator(skip_on_failure=True)
    def validate_name(cls, values):
        if not values.get('name'):
            raise ValueError('Поле name содержит цифры')
        surname = ''.join(values['surname'])
        checked_values = values['name'] + surname
        if (
                re.search('[a-z]', checked_values, re.IGNORECASE)
                and
                re.search('[а-я]', checked_values, re.IGNORECASE)
        ):
            raise ValueError('Не смешивайте буквы')
        return values
