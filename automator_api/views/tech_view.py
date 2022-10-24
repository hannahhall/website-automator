from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from automator_api.models import Tech
from automator_api.serializers import TechSerializer
from .admin_or_read_only import IsAdminOrReadOnly


class TechViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    List, Create Methods for Tech model
    """
    queryset = Tech.objects.all()
    serializer_class = TechSerializer
    permission_classes = [IsAdminOrReadOnly]
