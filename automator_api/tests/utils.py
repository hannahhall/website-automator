from django.contrib.auth import get_user_model


def create_test_user():
    """Create and return a new test user

    Returns:
        User: the new user object
    """
    return get_user_model().objects.create_user(
        username='testUser',
        first_name='Test',
        last_name='McTestson',
        email='test@test.com',
        password='test1234',
        is_staff=True
    )
