# Generated by Django 4.1.1 on 2022-10-03 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('demo_day', models.DateField(null=True)),
                ('demo_day_time', models.TimeField(null=True)),
                ('demo_day_link', models.URLField(default='http://nashss.com/demoday')),
                ('slack_channel', models.CharField(max_length=50)),
                ('github_organization', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tech',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('text', models.CharField(max_length=50)),
                ('icon', models.ImageField(upload_to='techs/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('student_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('github_handle', models.CharField(max_length=75)),
                ('image', models.ImageField(blank=True, null=True, upload_to='students/')),
                ('linkedin', models.CharField(max_length=75)),
                ('resume_link', models.URLField(blank=True, null=True)),
                ('podcast_link', models.URLField(blank=True, null=True)),
                ('favorite_quote', models.CharField(blank=True, max_length=100, null=True)),
                ('cohort', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='automator_api.cohort')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('deployed_url', models.URLField(blank=True, null=True)),
                ('github_url', models.URLField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='automator_api.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProgramTech',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='automator_api.program')),
                ('tech', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='automator_api.tech')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='program',
            name='techs',
            field=models.ManyToManyField(through='automator_api.ProgramTech', to='automator_api.tech'),
        ),
        migrations.CreateModel(
            name='CohortWebsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deployed', models.BooleanField(default=False)),
                ('short_url', models.URLField(null=True)),
                ('cohort', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='automator_api.cohort')),
                ('theme', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='automator_api.theme')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cohort',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cohorts', to='automator_api.program'),
        ),
    ]
