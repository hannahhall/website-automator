
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from automator_api.serializers import user_serializers as serializers


class UsersView(ViewSet):
    """User View

    actions:
        profile (GET): Get current user's information
    """
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False)
    def profile(self, request):
        """Responds with the current user's information
        """
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)
