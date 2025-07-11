from rest_framework import serializers
from .models import Movie

class VfxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title','imgsrc', 'actualimage', 'desc', 'year', 'showcase_picture_credits', 'directors' ,'producers','vfx_supervisors','vfx_producers','animation_supervisors']

