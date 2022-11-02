from django.db import models
from .timestamp_mixin import TimestampMixin


class Cohort(TimestampMixin):
    """Cohort Model

    Fields:
        demo_day (DateField): The date of the cohort's demo day
        demo_day_link (CharField): The Eventbrite link to register
        demo_day_time (TimeField): The start time of demo day
        github_organization (CharField): The name of the cohort's github org
        name (CharField)
        program (ForeignKey)
        slack_channel (CharField): The cohort's main slack channel
    """
    name = models.CharField(max_length=100)
    demo_day = models.DateField(null=True)
    demo_day_time = models.TimeField(null=True)
    demo_day_link = models.URLField(default='http://nashss.com/demoday')
    slack_channel = models.CharField(max_length=50)
    github_organization = models.CharField(max_length=100)
    program = models.ForeignKey(
        'Program', on_delete=models.DO_NOTHING, related_name='cohorts')
    techs = models.ManyToManyField('Tech')

    def __str__(self):
        return f'{self.name} - {self.program.name}'
