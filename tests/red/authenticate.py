import pytest

from src.services.user_service import register_user, authenticate


def test_success_login(uniq_email, origin_pass):
    email = uniq_email
    password = origin_pass

    login_user = register_user(
        email=uniq_email,
        password=password,
        full_name='Testing User'
    )

    authenticate_user = authenticate(
        email=email,
        password=password
    )

    assert login_user.id == authenticate_user.id


def test_wrong_password(uniq_email, origin_pass):
    email = uniq_email
    password = origin_pass

    register_user(
        email=email,
        password=password,
        full_name='Testing User'
    )

    with pytest.raises(ValueError):
        authenticate(
            email=email,
            password='$WWWWWrongPassword141'
        )


def test_wrong_email(uniq_email, origin_pass):
    password = origin_pass

    register_user(
        email=uniq_email,
        password=password,
        full_name='Testing User'
    )

    with pytest.raises(ValueError):
        authenticate(
            email='try_this@email.com',
            password=password
        )
