import json
import requests
from time import sleep

from rest_framework import serializers
from automator_api.models import Cohort


class CohortListSerializer(serializers.ModelSerializer):
    """Cohort Model Serializer for list view

    Fields:
        id, name
    """
    class Meta:
        model = Cohort
        fields = ('id', 'name', 'demo_day')


class CohortCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ('id', 'name', 'demo_day', 'demo_day_time', 'github_organization',
                  'slack_channel', 'program', 'techs')

    