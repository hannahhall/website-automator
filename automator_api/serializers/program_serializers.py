from rest_framework import serializers
from automator_api.models import Program
from .cohort_serializers import CohortListSerializer


class ProgramListSerializer(serializers.ModelSerializer):
    """Program Model Serializer for list view

    Fields:
        id, name
    """
    class Meta:
        model = Program
        fields = ('id', 'name')


class ProgramRetrieveSerializer(serializers.ModelSerializer):
    """Program Model Serializer for list view

    Fields:
        id, name
    """
    cohorts = CohortListSerializer(many=True)

    class Meta:
        model = Program
        fields = ('id', 'name', 'cohorts', 'techs')
        depth = 1
