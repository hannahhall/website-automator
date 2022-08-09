import uuid
from django.conf import settings
from django.db import models
from .timestamp_mixin import TimestampMixin


class Student(TimestampMixin):
    """Student Model

    Fields:
        bio (TextField)
        cohort (ForeignKey)
        github_handle (CharField)
        image (ImageField): Profile image, uploaded to Cloudinary
        linkedin (CharField): LinkedIn username
        podcast_link (URLField)
        resume_link (URLField)
        student_id (UUIDField): Unique key for students
        user (OneToOneField)
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    bio = models.TextField(null=True, blank=True)
    github_handle = models.CharField(max_length=75)
    image = models.ImageField(upload_to='students/', null=True, blank=True)
    linkedin = models.CharField(max_length=75)
    resume_link = models.URLField(null=True, blank=True)
    podcast_link = models.URLField()
    cohort = models.ForeignKey('Cohort', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text
