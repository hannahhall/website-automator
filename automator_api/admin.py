from django.contrib import admin
from automator_api import models

# Register your models here.
admin.site.register(models.Cohort)
admin.site.register(models.CohortWebsite)
admin.site.register(models.Program)
admin.site.register(models.Project)
admin.site.register(models.Student)
admin.site.register(models.Tech)
admin.site.register(models.Theme)
