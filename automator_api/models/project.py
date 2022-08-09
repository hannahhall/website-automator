from django.db import models
from .timestamp_mixin import TimestampMixin


class Project(TimestampMixin):
    """Student Project Model

    Fields:
        description (CharField)
        image (ImageField)
        student (ForeignKey)
    """
    description = models.CharField(max_length=255)
    image = models.ImageField()
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.text
