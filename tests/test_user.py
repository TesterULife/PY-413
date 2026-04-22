from src.engine import sync_session_factory
from src.models.user import User
from src.services.user_service import register_user, soft_delete_user, restore_user


def test_soft_delete_user(uniq_email):
    target_user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='Testing User'
    )

    soft_delete_user(target_user.id)

    with sync_session_factory() as session:
        user = session.get(User, target_user.id)

        assert user.is_deleted is True


def test_restore_user(uniq_email):
    target_user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='Testing User'
    )

    user_id = target_user.id

    soft_delete_user(user_id)

    with sync_session_factory() as session:
        user = session.get(User, user_id)

        assert user is not None
        assert user.is_deleted is True

    restore_user(user_id=user_id)

    with sync_session_factory() as session:
        user = session.get(User, user_id)

        assert user is not None
        assert user.is_deleted is False
