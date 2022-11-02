from rest_framework import status
from django.urls import reverse
from automator_api.models import Tech, Program
from .. import utils


class TestProgramView(utils.AutomatorAPITestCase):
    """Test for Program View
    """
    fixtures = ['techs', 'programs', 'cohorts']

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

    def test_remove_tech(self):
        """Test that the tech is removed from a program
        """
        program = Program.objects.first()
        tech_to_remove = program.techs.first()

        url = reverse('program-techs',
                      kwargs={'pk': program.id, 'tech_pk': tech_to_remove.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        program.refresh_from_db()

        self.assertNotIn(tech_to_remove, program.techs.all())
