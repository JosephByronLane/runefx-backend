# Generated by Django 5.2 on 2025-07-01 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('releases', '0003_alter_release_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='showcase_picture_url_credits',
            field=models.CharField(default='test'),
            preserve_default=False,
        ),
    ]
