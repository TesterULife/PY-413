import uuid

import bcrypt
import pytest

from src.engine import sync_session_factory
from src.models.role import Role
from src.models.user import User
from src.services.user_service import register_user
from src.services.crud_roles import create_role


@pytest.fixture
def uniq_email():
    email = f"{uuid.uuid4()}@gmail.com"

    return email


@pytest.fixture
def origin_pass():
    password = '123AD345'

    hash_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    return hash_password


@pytest.fixture
def admin(password='PassWord'):
    email = f"{uuid.uuid4()}@gmail.com"

    register_user(
        email=email,
        password=password,
        full_name='Admin'
    )

    with sync_session_factory() as session:
        user = session.query(User).filter_by(email=email).first()

        admin_role = session.query(Role).filter_by(name_role='admin').first()

        if not admin_role:
            admin_role = Role(name_role='admin')
            session.add(admin_role)
            session.commit()

        user.roles.append(admin_role)
        session.commit()

        user_id = user.id
        return user_id


@pytest.fixture(scope='session', autouse=True)
def setup_roles():
    with sync_session_factory() as session:
        if not session.query(Role).filter_by(name_role='user').first():
            session.add(Role(name_role='user'))

        if not session.query(Role).filter_by(name_role='admin').first():
            session.add(Role(name_role='admin'))

        session.commit()


@pytest.fixture
def uniq_role(admin):
    role = create_role(
        admin_id=admin,
        name=f'test_role_{uuid.uuid4()}',
        description='role for delete test'
    )

    return role