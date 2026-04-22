import logging
from pathlib import Path

import bcrypt
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import UUID

from src.engine import sync_session_factory
from src.models.role import Role
from src.models.user import User
from src.models.userrole import UserRole

"""
2. Регистрация пользователя
Напишите функцию register_user(email, password, full_name), которая:

Валидирует формат email.
Хеширует пароль (bcrypt или аналог).
Создаёт запись в User и связанную запись в Profile.
По умолчанию присваивает роль «user» (через UserRole).
"""

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "services.log"

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)


def register_user(email: str, password: str, full_name: str):
    try:
        valid_email = validate_email(email).email
    except EmailNotValidError as e:
        logger.error("Invalid email during register_user: %s", email)
        raise ValueError("Invalid email") from e

    hash_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    with (sync_session_factory() as session):
        with session.begin():

            existing_user = session.query(
                User
            ).filter_by(
                email=valid_email
            ).first()

            if existing_user:
                logger.warning(
                    "Email already registered: %s",
                    email,
                )
                raise ValueError("Email already registered")

            user = User(
                email=valid_email,
                password=hash_password,
                username=full_name
            )
            session.add(user)
            session.flush()

            role = session.query(Role).filter_by(name_role='user').first()

            if not role:
                logger.error(
                    "Default role 'user' not found for email=%s",
                    valid_email
                )
                raise ValueError("Default role 'user' not found")

            user_role = UserRole(
                user_id=user.id,
                role_id=role.id
            )

            session.add(user_role)
            session.refresh(user)

            return user


"""
3. Авторизация и проверка пароля
Реализуйте функцию authenticate(email, password), которая:

Ищет пользователя по email.
Проверяет хеш пароля.
Возвращает объект пользователя или ошибку.
"""


def authenticate(email: str, password: str):
    with sync_session_factory() as session:
        user = session.query(User).filter_by(email=email, is_deleted=False).first()

        if not user:
            raise ValueError("Email not found")

        if not bcrypt.checkpw(
                password.encode(),
                user.password.encode() if isinstance(user.password, str)
                else user.password
        ):
            logger.warning(
                "This password is incorrect=%s",
                password,
            )
            raise ValueError("Incorrect password")

        return user


"""
8. Удаление и восстановление пользователей
Добавьте флаг is_deleted в модель User.

soft_delete_user(user_id) 
— отмечает пользователя удалённым, но не стирает данные.

restore_user(user_id) 
— снимает флаг. Запрещает регистрацию
 нового пользователя с тем же email, пока старый не удалён.
"""


def soft_delete_user(user_id: UUID):
    with sync_session_factory() as session:
        with session.begin():
            user = session.query(User).filter_by(id=user_id).first()

            if not user:
                raise ValueError('User_id not found')

            user.is_deleted = True

            session.commit()

            return user


def restore_user(user_id: UUID):
    with sync_session_factory() as session:
        with session.begin():
            user = session.query(User).filter_by(id=user_id).first()

            if not user:
                raise ValueError('User_id not found')

            existing_user = session.query(User).filter(
                User.email == user.email,
                User.id != user.id,
                User.is_deleted == False
            ).first()

            if existing_user:
                logger.warning(
                    "This email address already exists=%s",
                    existing_user.email,
                )
                raise ValueError('This email is already registered')

            user.is_deleted = False

            session.commit()

            return user
