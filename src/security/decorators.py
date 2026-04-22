from functools import wraps
from typing import Callable
from src.engine import sync_session_factory
from src.models.user import User
from sqlalchemy.orm import selectinload
import inspect # подгрузка данных, чтобы не делать отдельные запросы

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
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            admin_id = bound.arguments.get("admin_id")

            if not admin_id:
                raise Exception("admin is required")

            with sync_session_factory() as session:
                user = session.query(User).options(
                    selectinload(User.roles)
                ).filter_by(id=admin_id).first()

                if not user:
                    raise Exception("User not found")

                user_roles = user.roles

                if not any(role.name_role in roles for role in user_roles):
                    raise Forbidden("Access denied")

                return func(*args, **kwargs)

        return wrapper

    return decorator


class Forbidden(Exception):
    pass
