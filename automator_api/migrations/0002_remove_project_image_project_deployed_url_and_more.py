# Generated by Django 4.1 on 2022-08-23 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automator_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='image',
        ),
        migrations.AddField(
            model_name='project',
            name='deployed_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='github_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='title',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tech',
            name='icon',
            field=models.ImageField(upload_to='techs/'),
        ),
    ]