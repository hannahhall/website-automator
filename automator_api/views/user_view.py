from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from automator_api.serializers import user_serializers as serializers
from automator_api.models import Student


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

    @action(methods=['get'], detail=False)
    def student(self, request):
        try:
            student = Student.objects.get(user=request.user)
            if 'expand' in request.query_params:
                serializer = serializers.StudentDetailSerializer(student)
            else:
                serializer = serializers.UpdateStudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=False, url_path='student-update')
    def student_update(self, request):
        try:
            student = Student.objects.get(user=request.user)
            serializer = serializers.UpdateStudentSerializer(
                student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Student.DoesNotExist:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
