from django.db import models
from django.conf import settings
class Release(models.Model):
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    showcase_picture_url =  models.CharField(
        blank=False,
        null=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True

    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank = False,
        null = False
    )


    content = models.TextField(
        blank=False,
        null=False,
        help_text="Release note's content. Markdown supported"
    )


    def __str__(self):
        return self.title
    
