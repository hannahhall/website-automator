from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from automator_api.models import Student


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


def create_test_student():
    user = get_user_model().objects.create_user(
        username='testStudent',
        first_name='Student',
        last_name='McTestson',
        email='test@test.com',
        password='test1234',
        is_staff=False
    )

    return Student.objects.create(
        user=user,
        github_handle='githubUsername',
        linkedin='linkedinUsername',
        cohort_id=1,
    )


def login(user, client):
    url = reverse('token_obtain_pair')
    response = client.post(
        url, {'username': user.username, 'password': 'test1234'}, format='json')
    token = response.data['access']

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


class AutomatorAPITestCase(APITestCase):
    """Test class that will set up an initial user and add token to client
    """

    def setUp(self):
        super().setUp()
        self.user = create_test_user()
        self.student = create_test_student()
        login(self.user, self.client)
