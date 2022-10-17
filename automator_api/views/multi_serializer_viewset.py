from rest_framework import viewsets


class MultiSerializerViewSet(viewsets.ModelViewSet):
    """Add multiple serializers to a ModelViewSet
    """
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(
            self.action,
            self.serializers['default']
        )
