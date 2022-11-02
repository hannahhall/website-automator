from rest_framework import status

from automator_api.serializers import UserSerializer
from ..utils import AutomatorAPITestCase


class TestUserView(AutomatorAPITestCase):
    """Test for register functions
    """
    fixtures = ['techs', 'programs', 'cohorts']

    def test_get_profile(self):
        """Test for getting the current users profile
        """
        response = self.client.get('/api/users/profile')
        expected = UserSerializer(self.user)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected.data, response.data)
