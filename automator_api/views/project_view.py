from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets

from automator_api.models import Project
from automator_api.serializers import ProjectSerializer


class ProjectViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    Retrieve, Update, Create, Delete Projects
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
