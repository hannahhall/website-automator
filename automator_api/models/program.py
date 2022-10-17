from django.db import models
from .timestamp_mixin import TimestampMixin


class Program(TimestampMixin):
    """Program Model

    Fields:
        name (CharField): the program name
    """
    name = models.CharField(max_length=100)
    techs = models.ManyToManyField('Tech', through='ProgramTech')

    def __str__(self):
        return self.name
