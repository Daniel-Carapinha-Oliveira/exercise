import pytest

from django.contrib.auth import get_user_model

from apps.core.helpers import get_deleted_user

User = get_user_model()
pytestmark = pytest.mark.django_db


class TestGetDeletedUserHelper:
    def test_user_does_not_exist_function_must_create_it(self):
        user = User.objects.filter(username="deleted_user").first()
        assert user is None

        get_deleted_user()
        user = User.objects.filter(username="deleted_user").first()
        assert user is not None

    def test_user_already_exists_function_must_return_it(self, user_factory):
        created_user = user_factory(
            username="deleted_user",
            first_name='Deleted',
            last_name='User',
            email='deleted_user@deleted_user.com',
            is_superuser=False,
            is_staff=False,
            is_active=False
        )

        deleted_user = get_deleted_user()

        assert created_user == deleted_user