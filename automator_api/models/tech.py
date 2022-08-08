from django.db import models


class Tech(models.Model):
    text = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.text
