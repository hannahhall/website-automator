from django.db import models
from .timestamp_mixin import TimestampMixin


class CohortWebsite(TimestampMixin):
    """CohortWebsite Model

    Fields:
        cohort (ForeignKey)
        is_deployed (BooleanField): Whether the website is deployed
        short_url (URLField): The url that Mandy creates for the website
        theme (ForeignKey)
    """
    cohort = models.OneToOneField('Cohort', on_delete=models.CASCADE, editable=False)
    is_deployed = models.BooleanField(default=False)
    short_url = models.URLField(null=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_DEFAULT, default=1)

    @property
    def url(self):
        """The github website url based on the cohort's gh organization name

        Returns:
            string: The Class website url
        """
        return f'https://{self.cohort.github_organization}.github.io'

    def __str__(self):
        return self.cohort.name
