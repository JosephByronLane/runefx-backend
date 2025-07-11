from rest_framework import serializers
from .models import Movie, Director
class VfxSerializerDetail(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()
    producers = serializers.SerializerMethodField()
    vfx_supervisors = serializers.SerializerMethodField()
    vfx_producers = serializers.SerializerMethodField()
    animation_supervisors = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'imgsrc', 'actualimage', 'desc', 'year', 'directors', 'producers', 'vfx_supervisors', 'vfx_producers', 'animation_supervisors']

    def get_directors(self, obj):
        directors = obj.directors.all()
        return [director.name for director in directors]
    
    
    def get_producers(self, obj):
        producers = obj.producers.all()
        return [director.name for director in producers]
    
    def get_vfx_supervisors(self, obj):
        vfx_supervisors = obj.vfx_supervisors.all()
        return [director.name for director in vfx_supervisors]
    
    def get_vfx_producers(self, obj):
        vfx_producers = obj.vfx_producers.all()
        return [director.name for director in vfx_producers]
    
    def get_animation_supervisors(self, obj):
        animation_supervisors = obj.animation_supervisors.all()
        return [director.name for director in animation_supervisors]
class VfxSerializerBase(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'imgsrc', 'year']


