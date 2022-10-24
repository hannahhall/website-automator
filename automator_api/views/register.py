import os

from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
        Response: User tokens, 201
    """
    try:
        password_validation.validate_password(request.data['password'])
    except ValidationError as ex:
        return Response({'password': ex.messages[0]}, status=status.HTTP_400_BAD_REQUEST)

    if int(request.data.get('is_staff')):
        if request.data.get('instructor_password') == os.environ.get('INSTRUCTOR_PASSWORD'):
            new_user = create_instructor(request.data)
        else:
            return Response(
                {'instructor_password': 'Please reach out to #class-website-automator for help'},
                status=status.HTTP_403_FORBIDDEN
            )
    else:
        new_user = create_student(request.data)

    token = TokenObtainPairSerializer.get_token(new_user)

    return Response({
        'access': str(token.access_token),
        'refresh': str(token)
    }, status=status.HTTP_201_CREATED)


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
    serializer.save(user=user)

    return user


def create_user(data):
    """Create the django User

    Args:
        data (dict): request data

    Returns:
        User: user object that was created
    """
    return get_user_model().objects.create_user(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
    )
