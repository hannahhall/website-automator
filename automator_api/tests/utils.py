from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase


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


class AutomatorAPITestCase(APITestCase):
    """Test class that will set up an initial user and add token to client
    """

    def setUp(self):
        super().setUp()
        self.user = create_test_user()
        url = reverse('token_obtain_pair')
        response = self.client.post(
            url, {'username': self.user.username, 'password': 'test1234'}, format='json')
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
