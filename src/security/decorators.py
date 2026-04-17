from functools import wraps
from typing import Callable

"""
6. Ограничение доступа по ролям
Опишите декоратор @requires_roles(*roles), 
который оборачивает функцию-обработчик и проверяет, 
что текущий пользователь имеет хотя бы одну из указанных ролей, 
иначе выбрасывает Forbidden.
"""


def requires_roles(*roles):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user')

            if not user:
                raise Exception("User is required")

            user_roles = user.roles

            if not any(role in user_roles for role in roles):
                raise Forbidden("Access denied")

            return func(*args, **kwargs)

        return wrapper

    return decorator


class Forbidden(Exception):
    pass
