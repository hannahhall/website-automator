from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets

from automator_api.models import Project, Student
from automator_api.serializers import ProjectSerializer


class ProjectViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    Retrieve, Update, Create, Delete Projects
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """The logged in student should only be able to access their projects"""
        try:
            student = Student.objects.get(user=self.request.user)
            return Project.objects.filter(student=student)
        except Student.DoesNotExist:
            return []
