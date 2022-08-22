from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import ValidationError
# from automator_api.models import 
# from automator_api.serializers import Serializer
class UsersView(ViewSet):
    @action(methods=['get'], detail=False)
    def profile(self, request):
        return Response({'auth': True})
