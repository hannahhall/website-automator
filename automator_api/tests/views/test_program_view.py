from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from automator_api.models import Tech, Program
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

    def test_program_create(self):
        """Test creating a program with techs
        """
        data = {
            'name': 'Web Dev',
            'techs': [tech.id for tech in Tech.objects.all()[:1]]
        }

        response = self.client.post('/api/programs', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['techs'], data['techs'])

    def test_program_create_no_techs(self):
        """Test creating a program without adding techs does not error
        """
        data = {
            "name": "Web Dev"
        }

        response = self.client.post('/api/programs', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['techs'])

    def test_update_program(self):
        """Test updating a program
        """
        program = Program.objects.first()

        data = {
            'name': f'{program.name} updated',
            'techs': [tech.id for tech in Tech.objects.all()[2:4]]
        }

        response = self.client.put(
            f'/api/programs/{program.id}', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['techs'], data['techs'])
        self.assertEqual(response.data['name'], data['name'])
