from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    
    bio = models.TextField(
        null=True,
        blank=True,
        max_length=240,
        help_text='Users bio. Can be thought of as a short description of the user',
    )

    first_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text='Users first name',
    )
    
    last_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text='Users last name',
    )

    def user_profile_picture_path(instance, filename):
        #final filepath is MEDIA_ROOT/users/user_id/profile_pictures/filename
        return f'users/{instance.id}/profile_pictures/{filename}'
    
    profile_picture_url = models.CharField(
        null=True,
        blank=True,
        help_text='Users profile picture',
    )
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=ROLE_CHOICES,
        help_text='Users role',
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        help_text='Users email',
    )


    def __str__(self):
        return self.username
    
    



