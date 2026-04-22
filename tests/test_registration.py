import pytest

from src.engine import sync_session_factory
from src.models.user import User
from src.services.user_service import register_user


def test_registration_user(uniq_email):
    email = uniq_email()

    user = register_user(
        email=email,
        password='PassWord',
        full_name='Testing User'
    )

    assert user is not None
    assert user.email == email


def test_registration_user_invalid_email():
    with pytest.raises(ValueError):
        register_user(
            email='@John.com',
            password='PassWord',
            full_name='Testing User'
        )


def test_duplicate_email(uniq_email):
    target_email = uniq_email()

    register_user(
        email=target_email,
        password='PassWord',
        full_name='Testing User'
    )

    with pytest.raises(ValueError):
        register_user(
            email=target_email,
            password='PaSsWord',
            full_name='User John'
        )


def test_default_role(uniq_email):
    email = uniq_email()

    register_user(
        email=email,
        password='PassWord',
        full_name='Testing User'
    )

    with sync_session_factory() as session:
        user = session.query(User).filter_by(email=email).first()

        assert user.roles is not None
        assert len(user.roles) == 1
        assert user.roles[0].name_role == 'user'