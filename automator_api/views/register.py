import os

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from automator_api.serializers import user_serializers as serializers


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new student or instructor

    Returns:
        Response: Serialized user, 201
    """
    if request.data.get('instructor_password') == os.environ.get('INSTRUCTOR_PASSWORD'):
        new_user = create_instructor(request.data)
    else:
        new_user = create_student(request.data)

    serializer = serializers.UserSerializer(new_user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


def create_instructor(data):
    """Create a user object for instructor, save is_staff=True

    Args:
        data (dict): data from request

    Returns:
        User: the created User object
    """
    user = create_user(data)
    user.is_staff = True
    user.save()

    return user


def create_student(data):
    """Create the Student object

    Args:
        data (dict): request data

    Returns:
        user: the User object
    """
    user = create_user(data)
    serializer = serializers.CreateStudentSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    student = serializer.save(user=user)

    if data.get('image'):
        student.save_profile_image(data['image'])

    return user


def create_user(data):
    """Create the django User

    Args:
        data (dict): request data

    Returns:
        User: user object that was created
    """
    return get_user_model().objects.create(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
    )