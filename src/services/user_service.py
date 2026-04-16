import bcrypt
from email_validator import validate_email, EmailNotValidError
import logging

from src.engine import sync_session_factory
from src.models.profile import Profile
from src.models.role import Role
from src.models.user import User
from src.models.userrole import UserRole


"""
реализуйте функцию authenticate(email, password), которая:
Ищет пользователя по email.
Проверяет хеш пароля.
Возвращает объект пользователя или ошибку.
"""

logging.basicConfig(
    level=logging.INFO,
    filename='services.log',
    filemode='a',
    format="%(asctime)s - %(levelname)s - %(message)s",
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

    with sync_session_factory() as session:
        user = User(
            email=valid_email,
            password=hash_password,
            username=full_name
        )
        session.add(user)
        session.flush()

        profile = Profile(
            user_id=user.id,
            bio=None
        )
        session.add(profile)

        role = session.query(Role).filter_by(status_role='user').first()

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
        session.commit()
        return user


def remove_role(user_id: int, role_name: str):
    with (sync_session_factory() as session):
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            raise ValueError('User not found')

        role = session.query(Role).filter_by(name_role=role_name).first()

        if not role:
            raise ValueError('Role not found')

        user_role = session.query(UserRole).filter_by(
            user_id=user_id, role_id=role.id
        ).first()

        if not user_role:
            raise ValueError("This user doesn't have this role")

        user_roles = session.query(UserRole).filter_by(user_id=user_id).all()

        if len(user_roles) <= 1:
            logger.warning(
                "Attempt to remove last role from user_id=%s",
                user_id
            )
            raise ValueError("Can't remove last role")

        session.delete(user_role)
        session.commit()
