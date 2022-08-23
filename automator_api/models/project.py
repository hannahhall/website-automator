from django.db import models
from .timestamp_mixin import TimestampMixin


class Project(TimestampMixin):
    """Student Project Model

    Fields:
        title (CharField)
        description (CharField)
        student (ForeignKey)
        deployed_url (URLField)
        github_url (URLField)
    """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='projects')
    deployed_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.text
