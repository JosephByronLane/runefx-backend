from rest_framework import serializers
from .models import Topic, Subtopic, Post, Comment




class TopicSerializer(serializers.ModelSerializer):
    subtopics = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Topic
        fields = ['id', 'title', 'description','subtopics']

    def get_subtopics(self, obj):
        subtopics = Subtopic.objects.filter(parent_topic=obj.id)
        return SubtopicSerializer(subtopics, many=True, context=self.context).data


class SubtopicSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    child_subtopics = serializers.SerializerMethodField()

    class Meta:
        model = Subtopic
        fields = ['id', 'title', 'description', 'parent_subtopic','child_subtopics']

    def get_child_subtopics(self,obj):
        children = Subtopic.objects.filter(parent_subtopic=obj.id)
        return SubtopicSerializer(children, many=True, context=self.context).data
    
    def validate(self, data):
        if 'parent_topic' not in data and 'parent_subtopic' not in data:
            raise serializers.ValidationError("Subtopic must belong to a Topic, or Subtopic.")
        
        if 'parent_subtopic' in data and 'parent_topic' in data:
            raise serializers.ValidationError("Subtopic cannot belong to both a Topic and Subtopic.")
        
        return data
    
    def get_posts(self, obj):
        posts = Post.objects.filter(subtopic=obj.id)
        return PostSerializer(posts, many=True, context=self.context).data

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'subtopic', 'comments','created_by']
        read_only_fields = ['created_at', 'updated_at', 'creatded_by']

    def get_comments(self,obj):
        raise NotImplementedError("Comments are not implemented yet.")
    
    def validate(self, attrs):
        if 'subtopic' not in attrs and 'topic' not in attrs:
            raise serializers.ValidationError("Post must belong to a Topic or Subtopic.")
        
        if 'subtopic' in attrs and 'topic' in attrs:
            raise serializers.ValidationError("Post cannot belong to both a Topic and Subtopic.")
        
        return attrs
    
    