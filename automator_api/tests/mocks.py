# pylint: skip-file
from django.contrib.auth import get_user_model
from automator_api import models

def mock_user(_):
    return get_user_model().objects.first()


def mock_student(user=None):
    return models.Student.objects.first()


def mock_is_valid(raise_exception=False):
    return True


def mock_environ_get(_):
    return 'password'


def mock_save_image(_):
    pass
