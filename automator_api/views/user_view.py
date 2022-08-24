from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from automator_api.serializers import user_serializers as serializers


class UsersView(ViewSet):
    """User View

    actions:
        profile (GET): Get current user's information
    """

    @action(methods=['get'], detail=False)
    def profile(self, request):
        """Responds with the current user's information
        """
        serializer = serializers.UserSerializer(request.auth.user)
        return Response(serializer.data)
