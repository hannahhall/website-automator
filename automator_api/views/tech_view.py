from functools import partial
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, response, status
from automator_api.models import Tech
from automator_api.serializers import TechSerializer
from .admin_or_read_only import IsAdminOrReadOnly


class TechViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    List, Create, Update Methods for Tech model
    """
    queryset = Tech.objects.all()
    serializer_class = TechSerializer
    permission_classes = [IsAdminOrReadOnly]

    def update(self, request, pk):
        """Update Tech object"""
        tech = Tech.objects.get(pk=pk)

        serializer = TechSerializer(tech, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(None, status=status.HTTP_204_NO_CONTENT)
