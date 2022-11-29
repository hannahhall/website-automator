from rest_framework import status

from automator_api.serializers import UserSerializer, StudentDetailSerializer, UpdateStudentSerializer
from ..utils import AutomatorAPITestCase, login


class TestUserView(AutomatorAPITestCase):
    """Test for register functions
    """
    fixtures = ['techs', 'programs', 'cohorts']

    def setUp(self):
        super().setUp()
        login(self.student.user, self.client)

    def test_get_profile(self):
        """Test for getting the current users profile
        """
        response = self.client.get('/api/users/profile')
        expected = UserSerializer(self.student.user)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected.data, response.data)

    def test_get_student_expanded(self):
        """Test for getting the current student's expanded profile
        """
        response = self.client.get('/api/users/student')
        expected = UpdateStudentSerializer(self.student)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected.data, response.data)

    def test_get_student_detail(self):
        """Test for getting the current student's details
        """
        response = self.client.get('/api/users/student?expand')
        expected = StudentDetailSerializer(self.student)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected.data, response.data)

    def test_student_not_found(self):
        """Test when student does not exist
        """
        login(self.user, self.client)
        response = self.client.get('/api/users/student')

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
