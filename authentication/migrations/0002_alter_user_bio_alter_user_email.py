# Generated by Django 5.2 on 2025-04-19 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, help_text='Users bio. Can be thought of as a short description of the user', max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Users email', max_length=254, unique=True),
        ),
    ]
