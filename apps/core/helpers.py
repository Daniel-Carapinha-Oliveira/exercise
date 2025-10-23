from django.contrib.auth import get_user_model

User = get_user_model()

def get_deleted_user():
    """
    Ensures there is a user in the database representing a "deleted" account.
    If a user with username 'deleted_user' already exists, it retrieves that user.
    Otherwise, it creates a new inactive, non-staff, non-superuser user with
    predefined name and email values.

    Returns the User object corresponding to the "deleted_user", either existing
    or newly created.
    """
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