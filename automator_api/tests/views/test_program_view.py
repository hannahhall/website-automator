from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from automator_api.models import Tech
from .. import utils


class TestProgramView(APITestCase):
    """Test for Program View
    """
    fixtures = ['programs', 'cohorts', 'techs']

    def setUp(self):
        super().setUp()
        self.user = utils.create_test_user()
        url = reverse('token_obtain_pair')
        response = self.client.post(
            url, {'username': self.user.username, 'password': 'test1234'}, format='json')
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_program_create_serializer(self):
        """Test creating a program with techs
        """
        data = {
            "name": "Web Dev",
            "techs": [tech.id for tech in Tech.objects.all()]
        }

        response = self.client.post('/api/programs', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertTrue(response.data['techs'])

    def test_program_create_serializer_no_techs(self):
        """Test creating a program without adding techs does not error
        """
        data = {
            "name": "Web Dev"
        }

        response = self.client.post('/api/programs', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['techs'])
