from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    
    MAYA = 'maya'
    BLENDER = 'blender'
    Houdini = 'houdini'
    KATANA = 'katana'
    

    DCC_CHOICES = [
        (MAYA, 'Maya'),
        (BLENDER, 'Blender'),
        (Houdini, 'Houdini'),
        (KATANA, 'Katana'),
    ]
    dcc = models.CharField(max_length=255, 
                           null=False, 
                           blank=False, 
                           choices=DCC_CHOICES,

                           help_text='The primary DCC package used by the user',
                           )
    
    bio = models.TextField(
        null=True,
        blank=True,
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
    
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path,
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

    def __str__(self):
        return self.username
    
    



