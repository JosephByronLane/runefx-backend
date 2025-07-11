from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class VFXSupervisor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class VFXProducer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class AnimationSupervisor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    imgsrc = models.URLField(max_length=1024, blank=True, null=True)
    actualimage = models.URLField(max_length=1024, blank=True, null=True)
    desc = models.TextField()
    year = models.IntegerField()
    directors = models.ManyToManyField(Director, related_name='movies', blank=True)
    producers = models.ManyToManyField(Producer, related_name='movies', blank=True)
    vfx_supervisors = models.ManyToManyField(VFXSupervisor, related_name='movies', blank=True)
    vfx_producers = models.ManyToManyField(VFXProducer, related_name='movies', blank=True)
    animation_supervisors = models.ManyToManyField(AnimationSupervisor, related_name='movies', blank=True)

    def __str__(self):
        return self.title