from django.db import models
from cloudinary import CloudinaryImage

from .timestamp_mixin import TimestampMixin


class Tech(TimestampMixin):
    """Tech Model

    Fields:
        text (CharField): the tech name
        icon (URLField): The image location for the tech icon
    """
    text = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='techs/')

    def __str__(self):
        return self.text

    @property
    def square_icon(self):
        """Generates a square icon that is 100x100

        Returns:
            string: the url of the square icon
        """
        return CloudinaryImage(self.icon.name).build_url(aspect_ratio="1:1",
                                                         width=100, crop="fill")
