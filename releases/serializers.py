from rest_framework import serializers
from .models import Release

class ReleaseSerializer(serializers.ModelSerializer):


    class Meta:
        model = Release
        fields = ['id', 'title','created_at', 'created_by','content', 'showcase_picture_url']



class ReleaseSerializerWithoutContent(serializers.ModelSerializer):



    class Meta:
        model = Release
        fields = ['id', 'title', 'created_at', 'created_by', 'showcase_picture_url']



    