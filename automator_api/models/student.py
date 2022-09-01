import uuid
import base64
from django.conf import settings
from django.db import models
from django.core.files.base import ContentFile
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

    def save_profile_image(self, image_string):
        """Save the student's image to cloudinary

        Args:
            image_string (string): base64 encoded string
        """
        file_format, imgstr = image_string.split(';base64,')
        ext = file_format.split('/')[-1]
        image = ContentFile(base64.b64decode(imgstr),
                            name=f'{self.student_id}.{ext}')
        self.image = image
        self.save()
