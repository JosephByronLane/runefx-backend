# Generated by Django 5.2 on 2025-07-01 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('releases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='description',
            field=models.TextField(blank=True, help_text='Short description of what the patch notes might contain'),
        ),
    ]
