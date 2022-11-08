from rest_framework import serializers
from automator_api.models import Project


class CurrentStudentDefault(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        user = super().__call__(serializer_field)
        return user.student


class ProjectSerializer(serializers.ModelSerializer):
    """Project Model Serializer

    Fields:
        id, title, description, student, deployed_url, github_url
    """
    student = serializers.HiddenField(
        default=CurrentStudentDefault()
    )

    class Meta:
        model = Project
        fields = '__all__'
