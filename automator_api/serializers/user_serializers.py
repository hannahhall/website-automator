from django.contrib.auth import get_user_model
from rest_framework import serializers
from automator_api.models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Student model serializer

    fields: student_id, bio, github_handle, linkedin, resume_link,
            podcast_link, cohort, favorite_quote, image
    """
    class Meta:
        model = Student
        fields = ('student_id', 'bio', 'github_handle', 'linkedin', 'resume_link',
                  'podcast_link', 'cohort', 'favorite_quote', 'image')
        depth = 1


class CreateStudentSerializer(serializers.ModelSerializer):
    """Used in RegisterView

    fields: bio, github_handle, linkedin, resume_link,
            podcast_link, cohort, favorite_quote, image
    """
    class Meta:
        model = Student
        fields = ('bio', 'github_handle', 'linkedin', 'resume_link',
                  'podcast_link', 'cohort', 'favorite_quote', 'image')


class UserSerializer(serializers.ModelSerializer):
    """For UserView get and post responses

    fields: first_name, last_name, username, student, is_staff
    """
    student = StudentSerializer()

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'student', 'is_staff')
