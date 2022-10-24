from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from automator_api.models import Tech
from automator_api.tests import mocks
from .. import utils


class TestTechView(APITestCase):
    """Test for Tech View
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

    @mock.patch('cloudinary.CloudinaryImage.build_url', side_effect=mocks.mock_cloudinary_build_url)
    @mock.patch('os.environ.get',
                side_effect=mocks.mock_environ_get)
    def test_tech_list_method(self, mock_environ_get, mock_cloudinary):
        """Test list method returns expected keys
        """
        url = reverse('tech-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Tech.objects.count())

        tech_data = response.data[0]

        self.assertIn('square_icon', tech_data)
        self.assertIn('id', tech_data)
        self.assertIn('text', tech_data)

        mock_cloudinary.assert_called_with(
            aspect_ratio='1:1', width=100, crop='fill', cloud_name='password')

        mock_environ_get.assert_called_with('CLOUD_NAME')
