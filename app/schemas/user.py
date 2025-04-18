# app/schemas/user.py
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


# schemas.BaseUser — схема с базовыми полями модели пользователя
# (кроме пароля): id, email, is_active, is_superuser, is_verified.
# В квадратных скобках для аннотирования
# указывается тип данных для id пользователя,
# в нашем случае это int (Integer) — целое число.

# schemas.BaseUserCreate — схема для создания пользователя;
# в неё обязательно должны быть переданы email и password.
# Любые другие поля, передаваемые в запросе на создание пользователя,
# будут проигнорированы.

# schemas.BaseUserUpdate — схема для обновления объекта пользователя;
# содержит все базовые поля модели пользователя (в том числе и пароль).
# Все поля опциональны. Если запрос передаёт обычный
# пользователь (а не суперюзер), то поля
# is_active, is_superuser, is_verified
# исключаются из набора данных: эти три поля может изменить только суперюзер.