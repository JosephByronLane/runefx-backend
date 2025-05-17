from rest_framework import serializers
from .models import Topic, Subtopic, Post, Comment




class TopicSerializer(serializers.ModelSerializer):
   subtopics = serializers.SerializerMethodField()
   post = serializers.SerializerMethodField()
   created_by = serializers.ReadOnlyField(source='created_by.username')

   class Meta:
        model = Topic
        fields = ['id', 'title', 'description','subtopics']

