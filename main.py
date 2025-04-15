# main.py
from fastapi import FastAPI, Query, Body

from schemas import Person
app = FastAPI()


# Новый эндпоинт: приветствие для автора.
@app.get('/me', tags=['Специальный'], summary='Приветствие автора')
def hello_author():
    return {'Hello': 'author'}


@app.get('/math-sum')
def math_sum(
    add: list[float] = Query(..., gt=0, lt=9.99)
) -> float:
    return sum([num for num in add])


# @app.get(
#     '/{name}',
#     tags=['Common methods'],
#     summary='Общее приветствие',
#     response_description='Полная строка приветствия',
# )
# def greetings(
#     *,
#     name: str = Path(..., min_length=2, max_length=20, title='Полное имя', description='Можно вводить в любом регистре'),
#     surname: list[str] = Query(..., min_length=2, max_length=50),
#     cyrillic_string: str = Query('Здесь только кириллица', regex='^[А-Яа-яЁё ]+$'),
#     age: Optional[int] = Query(None, ge=4, le=99),
#     is_staff: bool = Query(False, alias='is-staff', include_in_schema=False),
#     education_level: Optional[EducationLevel] = None,
# ) -> dict[str, str]:
#     """
#         Приветствие пользователя:
#
#         - **name**: имя
#         - **surname**: фамилия
#         - **age**: возраст (опционально)
#         - **is_staff**: является ли пользователь сотрудником
#         - **education_level**: уровень образования (опционально)
#     """
#
#     surnames = ' '.join(surname)
#     result = ' '.join([name, surnames])
#     result = result.title()
#     if age is not None:
#         result += ', ' + str(age)
#     if education_level is not None:
#         # Чтобы текст смотрелся грамотно,
#         # переведём строку education_level в нижний регистр.
#         result += ', ' + education_level.lower()
#     if is_staff:
#         result += ', сотрудник'
#     return {'Hello': result}


# Меняем метод GET на POST, указываем статичный адрес.
@app.post('/hello')
# Вместо множества параметров теперь будет только один - person,
# в качестве аннотации указываем класс Person.
def greetings(person: Person = Body(
    ...,
    examples=Person.Config.schema_extra['examples']
    # examples={
    #     # Первый пример.
    #     'single_surname': {
    #         'summary': 'Одна фамилия',
    #         'description': 'Одиночная фамилия передается строкой',
    #         'value': {
    #             'name': 'Taras',
    #             'surname': 'Belov',
    #             'age': 20,
    #             'is_staff': False,
    #             'education_level': 'Среднее образование'
    #         }
    #     },
    #     # Второй пример.
    #     'multiple_surnames': {
    #         'summary': 'Несколько фамилий',
    #         'description': 'Несколько фамилий передаются списком',
    #         'value': {
    #             'name': 'Eduardo',
    #             'surname': ['Santos', 'Tavares'],
    #             'age': 20,
    #             'is_staff': False,
    #             'education_level': 'Высшее образование'
    #         }
    #     },
    #     # Третий пример.
    #     'invalid': {
    #         'summary': 'Некорректный запрос',
    #         'description': 'Возраст передается только целым числом',
    #         'value': {
    #             'name': 'Eduardo',
    #             'surname': ['Santos', 'Tavares'],
    #             'age': 'forever young',
    #             'is_staff': False,
    #             'education_level': 'Среднее специальное образование'
    #         }
    #     }
    # }
)
) -> dict[str, str]:
    # Обращение к атрибутам класса происходит через точку;
    # при этом будут работать проверки на уровне типов данных.
    # В IDE будут работать автодополнения.
    if isinstance(person.surname, list):
        surnames = ' '.join(person.surname)
    else:
        surnames = person.surname
    result = ' '.join([person.name, surnames])
    result = result.title()
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.education_level is not None:
        result += ', ' + person.education_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result}
