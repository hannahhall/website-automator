import base64
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from automator_api.models import Tech
from automator_api.serializers import TechSerializer


class TechViewSet(ViewSet):
    """
    List, Create
    """

    def list(self, request):
        """Get a list of all techs in the database
        """
        techs = Tech.objects.all()
        serializer = TechSerializer(techs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create a tech and upload the icon image to cloudinary
        """
        file_format, imgstr = request.data['icon'].split(';base64,')
        ext = file_format.split('/')[-1]
        file = ContentFile(base64.b64decode(imgstr),
                           name=f'{request.data["text"]}.{ext}')

        Tech.objects.create(
            text=request.data['text'],
            icon=file
        )

        return Response(status=status.HTTP_201_CREATED)
