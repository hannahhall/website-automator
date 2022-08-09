from django.db import models
from .timestamp_mixin import TimestampMixin


class Theme(TimestampMixin):
    """Theme Model

    Fields:
        name (CharField)
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
