from rest_framework import serializers
from automator_api.models import Tech


class TechSerializer(serializers.ModelSerializer):
    """Tech Model Serializer for view

    Fields:
        id, text, icon
    """
    class Meta:
        model = Tech
        fields = ('id', 'text', 'icon', 'square_icon')
