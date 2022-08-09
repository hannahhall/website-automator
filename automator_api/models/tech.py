from django.db import models
from .timestamp_mixin import TimestampMixin


class Tech(TimestampMixin):
    """Tech Model

    Fields:
        text (CharField): the tech name
        icon (URLField): The image location for the tech icon
    """
    text = models.CharField(max_length=50)
    icon = models.URLField()

    def __str__(self):
        return self.text
