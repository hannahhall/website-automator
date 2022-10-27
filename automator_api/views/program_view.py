from automator_api.models import Program
from automator_api.views.multi_serializer_viewset import MultiSerializerViewSet
from automator_api.serializers import (
    ProgramListSerializer, ProgramRetrieveSerializer, ProgramCreateUpdateSerializer)
from .admin_or_read_only import IsAdminOrReadOnly


class ProgramViewSet(MultiSerializerViewSet):
    """
    List, Retrieve, Update, Create, Delete Programs
    """
    queryset = Program.objects.all()
    serializers = {
        'default': ProgramListSerializer,
        'retrieve': ProgramRetrieveSerializer,
        'create': ProgramCreateUpdateSerializer,
        'update': ProgramCreateUpdateSerializer,
    }
    permission_classes = [IsAdminOrReadOnly]
