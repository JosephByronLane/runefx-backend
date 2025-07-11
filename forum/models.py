from django.db import models
from django.conf import settings

class Topic(models.Model):
    title = models.CharField(
        max_length=255,
        blank = False,
        null = False
    )
    description = models.TextField(
        max_length=255,
        blank = False,
        null = False
    )
    slug = models.CharField(
        max_length=60,
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
        on_delete=models.CASCADE,
        blank = False,
        null = False
    )

    def __str__(self):
        return self.title
    

class Subtopic(models.Model):
    title = models.CharField(
        max_length=200,
        blank=False,
        null=False
    )
    description = models.TextField(
        max_length=200,
        blank=False,
        null=False
    )

    slug = models.CharField(
        max_length=60,
        blank=False,
        null=False
    )

    parent_topic = models.ForeignKey(
        Topic,
        blank=True, #can be null because its either a parent topic, or a parent subtopic
        null=True,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE    
    )
      
    def __str__(self):
        return self.title
    
    def clean(self):
        if not  self.parent_topic:
            raise ValueError("A topic must have either a prent topic or subtopic")
        
        
class Post(models.Model):
    title = models.CharField(
        max_length=255,

    )
    
    content = models.TextField(
        blank=False,
        null=False,
        help_text="Markdown formatted text"
    )

    topic = models.ForeignKey(
        Topic,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts'               
    )    

    subtopic = models.ForeignKey(
        Subtopic,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    created_at = models.DateTimeField(
        auto_now=True,
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )

    def clean(self):
        if not self. parent_subtopic and self.parent_topic:
            raise ValueError("A topic must have either a prent topic or subtopic")
        
        if self.parent_topic and self.sub:
            raise ValueError("A topic cannot be part of a topic and a subtopic")
        
    def __srt__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField(
        blank=False,
        null=False,
        help_text="Markdown formatted text"
    )

    post = models.ForeignKey(
        Post,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    reply_to = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='replies'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,

    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Comment by {self.created_by} on {self.post}"

