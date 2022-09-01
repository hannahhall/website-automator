from rest_framework import serializers
from automator_api.models import Cohort


class CohortListSerializer(serializers.ModelSerializer):
    """Cohort Model Serializer for list view

    Fields:
        id, name
    """
    class Meta:
        model = Cohort
        fields = ('id', 'name')
