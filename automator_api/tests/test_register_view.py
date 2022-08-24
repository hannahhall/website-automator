from unittest import mock
from django.contrib.auth import get_user_model
from django.http import QueryDict
from rest_framework import status
from rest_framework.test import APITestCase

from automator_api.views import register
from automator_api.models import Student, Cohort
from automator_api.serializers import UserSerializer

from . import mocks


class TestUserView(APITestCase):
    """Test for register functions
    """
    fixtures = ['programs', 'cohorts']

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create(
            username='testUser',
            first_name='Test',
            last_name='McTestson',
            email='test@test.com',
            password='test1234',
        )

        self.student = Student.objects.create(
            user=self.user,
            github_handle="github_handle",
            linkedin="linkedin",
            cohort=Cohort.objects.first(),
            favorite_quote="Do or do not, there is no try"
        )

    def test_create_user(self):
        """Test that create_user returns the user object
        """
        data = {
            'username': 'test',
            'first_name': 'Test',
            'last_name': 'McTestson',
            'email': 'test@test.com',
            'password': 'test1234',
        }
        actual = register.create_user(data)

        expected = get_user_model().objects.get(
            username=data['username'])

        self.assertEqual(expected, actual)

    @mock.patch('automator_api.views.register.create_user',
                side_effect=mocks.mock_user)
    @mock.patch('automator_api.serializers.CreateStudentSerializer.save',
                side_effect=mocks.mock_student)
    @mock.patch('automator_api.serializers.CreateStudentSerializer.is_valid',
                side_effect=mocks.mock_is_valid)
    def test_create_student(self, mock_is_valid, mock_student, mock_user):
        """Test the create student return user
        """
        data = {
            'first_name': "test"
        }
        actual = register.create_student(data)

        mock_is_valid.assert_called_once_with(raise_exception=True)
        mock_student.assert_called_once_with(user=self.user)
        mock_user.assert_called_once_with(data)
        self.assertEqual(self.user, actual)

    @mock.patch('automator_api.views.register.create_user',
                side_effect=mocks.mock_user)
    def test_create_instructor(self, mock_user):
        """Test the create instructor return user and flips is_staff
        """
        data = {
            'first_name': "test"
        }
        actual = register.create_instructor(data)

        mock_user.assert_called_with(data)
        self.assertEqual(self.user, actual)
        self.assertTrue(actual.is_staff)

    @mock.patch('os.environ.get',
                side_effect=mocks.mock_environ_get)
    @mock.patch('automator_api.views.register.create_instructor',
                side_effect=mocks.mock_user)
    def test_register_instructor(self, mock_create_instructor, mock_environ_get):
        """Test POST request to register instructor
        """
        data = {
            'instructor_password': 'password'
        }

        query_dict = QueryDict('', mutable=True)
        query_dict.update(data)

        response = self.client.post('/api/register', data)

        mock_environ_get.assert_called_with('INSTRUCTOR_PASSWORD')
        mock_create_instructor.assert_called_with(query_dict)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        expected = UserSerializer(self.user)

        self.assertEqual(expected.data, response.data)

    @mock.patch('os.environ.get', side_effect=mocks.mock_environ_get)
    @mock.patch('automator_api.views.register.create_student',
                side_effect=mocks.mock_user)
    def test_register_student(self, mock_create_student, mock_environ_get):
        """Test POST request to register student
        """
        data = {
            'instructor_password': 'wrong'
        }

        query_dict = QueryDict('', mutable=True)
        query_dict.update(data)

        response = self.client.post('/api/register', data)

        mock_environ_get.assert_called_with('INSTRUCTOR_PASSWORD')
        mock_create_student.assert_called_with(query_dict)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        expected = UserSerializer(self.user)

        self.assertEqual(expected.data, response.data)
