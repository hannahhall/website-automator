from django.db import models
from .timestamp_mixin import TimestampMixin


class ProgramTech(TimestampMixin):
    """ProgramTech Model

    Fields:
        program (ForeignKey)
        tech (ForeignKey)
    """
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    tech = models.ForeignKey('Tech', on_delete=models.CASCADE)
