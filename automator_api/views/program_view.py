from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
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

    def get_queryset(self):
        queryset = Program.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    @action(methods=['DELETE'], detail=True, url_path=r'techs/(?P<tech_pk>[^/.]+)')
    def techs(self, request, pk, tech_pk):
        """Remove a single tech from the program
        """
        program = Program.objects.get(pk=pk)
        program.techs.remove(tech_pk)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
