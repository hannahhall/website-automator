import uuid
import os
from django.conf import settings
from django.db import models
from cloudinary import CloudinaryImage

from .timestamp_mixin import TimestampMixin


class Student(TimestampMixin):
    """Student Model

    Fields:
        bio (TextField)
        favorite_quote (CharField)
        cohort (ForeignKey)
        github_handle (CharField)
        image (ImageField): Profile image, uploaded to Cloudinary
        linkedin (CharField): LinkedIn username
        podcast_link (URLField)
        resume_link (URLField)
        student_id (UUIDField): Unique key for students
        user (OneToOneField)
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    bio = models.TextField(null=True, blank=True)
    github_handle = models.CharField(max_length=75)
    image = models.ImageField(upload_to='students/', null=True, blank=True)
    linkedin = models.CharField(max_length=75)
    resume_link = models.URLField(null=True, blank=True)
    podcast_link = models.URLField(null=True, blank=True)
    cohort = models.ForeignKey('Cohort', on_delete=models.DO_NOTHING)
    favorite_quote = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.get_full_name()

    @property
    def cohort_name(self):
        return self.cohort.name

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    def circle_image(self):
        return CloudinaryImage(self.image.name).build_url(width=256, height=256, radius="max", gravity="faces", crop="fill", cloud_name=os.environ.get("CLOUD_NAME"))
