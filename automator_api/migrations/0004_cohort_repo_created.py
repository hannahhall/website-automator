# Generated by Django 4.1.3 on 2022-12-01 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automator_api', '0003_cohort_is_deployed'),
    ]

    operations = [
        migrations.AddField(
            model_name='cohort',
            name='repo_created',
            field=models.BooleanField(default=False),
        ),
    ]
