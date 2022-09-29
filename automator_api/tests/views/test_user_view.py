from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from automator_api.serializers import UserSerializer
from ..utils import create_test_user


class TestUserView(APITestCase):
    """Test for register functions
    """
    fixtures = ['programs', 'cohorts']

    def setUp(self):
        super().setUp()
        self.user = create_test_user()
        url = reverse('token_obtain_pair')
        response = self.client.post(
            url, {'username': self.user.username, 'password': 'test1234'}, format='json')
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_profile(self):
        """Test for getting the current users profile
        """
        response = self.client.get('/api/users/profile')
        expected = UserSerializer(self.user)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected.data, response.data)
