from django.contrib.auth import get_user_model

User = get_user_model()

def get_deleted_user():
    user, created = User.objects.get_or_create(
        username = 'deleted_user',
        first_name = 'Deleted',
        last_name = 'User',
        email = 'deleted_user@deleted_user.com',
        is_superuser = False,
        is_staff = False,
        is_active = False
    )

    return user