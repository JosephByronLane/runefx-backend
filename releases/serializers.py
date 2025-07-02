from rest_framework import serializers
from .models import Release

class ReleaseSerializer(serializers.ModelSerializer):
    created_by_user_data = serializers.SerializerMethodField()
    class Meta:
        model = Release
        fields = ['id', 'title','created_at', 'created_by', 'content', 'showcase_picture_url', 'showcase_picture_credits', 'created_by_user_data' ,'description']
        read_only_fields = ['created_at', 'created_by']

    def get_created_by_user_data(self, obj):        
        if obj.created_by:
            return {
                'username': obj.created_by.username,
                'user_pfp_url': obj.created_by.profile_picture_url
            }


class ReleaseSerializerWithoutContent(serializers.ModelSerializer):
    created_by_user_data = serializers.SerializerMethodField()

    class Meta:
        model = Release
        fields = ['id', 'title', 'created_at', 'created_by', 'showcase_picture_url', 'created_by_user_data', 'showcase_picture_credits', 'description']
        read_only_fields = ['created_at', 'created_by']


    def get_created_by_user_data(self, obj):        
        if obj.created_by:
            return {
                'username': obj.created_by.username,
                'user_pfp_url': obj.created_by.profile_picture_url
            }

    