from automator_api.models import Cohort
from automator_api.views.multi_serializer_viewset import MultiSerializerViewSet
from automator_api.serializers import CohortListSerializer


class CohortViewSet(MultiSerializerViewSet):
    """
    List, Retrieve, Update, Create, Delete Cohorts
    """
    queryset = Cohort.objects.all()
    serializers = {
        'default': CohortListSerializer
    }
