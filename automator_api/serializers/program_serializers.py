from rest_framework import serializers
from automator_api.models import Program
from .cohort_serializers import CohortListSerializer
from .tech_serializers import TechSerializer


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
    techs = TechSerializer(many=True)

    class Meta:
        model = Program
        fields = ('id', 'name', 'cohorts', 'techs')
        depth = 1


class ProgramCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating a program

    fields:
        name, techs
    """
    class Meta:
        model = Program
        fields = ('id', 'name', 'techs')

    def save(self, **kwargs):
        """Override the save method to set the techs for a program

        Returns:
            Program: the object that was saved/updated
        """
        program = super().save(**kwargs)
        program.techs.set(self.initial_data.get('techs', []))
        return program
