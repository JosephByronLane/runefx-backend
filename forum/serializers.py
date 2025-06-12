from rest_framework import serializers
from .models import Topic, Subtopic, Post, Comment

CREATED_BY_USERNAME = 'created_by.username'

class TopicSerializer(serializers.ModelSerializer):
    subtopics = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'title', 'description','subtopics', 'posts', 'slug']

    def get_subtopics(self, obj):
        subtopics = Subtopic.objects.filter(parent_topic=obj.id)
        return SubtopicSerializer(subtopics, many=True, context=self.context).data
    
    def get_posts(self, obj):
        posts = Post.objects.filter(topic=obj.id)
        return PostSerializer(posts, many=True, context=self.context).data


class SubtopicSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    class Meta:
        model = Subtopic
        fields = ['id', 'title', 'description','parent_topic', 'posts', 'slug']

    def get_child_subtopics(self,obj):
        children = Subtopic.objects.filter(parent_subtopic=obj.id)
        return SubtopicSerializer(children, many=True, context=self.context).data
    
    def validate(self, data):
        if 'parent_topic' not in data :
            raise serializers.ValidationError("Subtopic must belong to a Topic.")

        return data
    
    def get_posts(self, obj):
        posts = Post.objects.filter(subtopic=obj.id)
        return PostSerializer(posts, many=True, context=self.context).data

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source=CREATED_BY_USERNAME)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'subtopic', 'comments','created_by']
        read_only_fields = ['created_at', 'updated_at', 'creatded_by']

    def get_comments(self,obj):
        comments = Comment.objects.filter(post=obj.id)
        return CommentSerializer(comments, many=True, context=self.context).data
    
    def validate(self, attrs):
        if 'subtopic' not in attrs and 'topic' not in attrs:
            raise serializers.ValidationError("Post must belong to a Topic or Subtopic.")
        
        if 'subtopic' in attrs and 'topic' in attrs:
            raise serializers.ValidationError("Post cannot belong to both a Topic and Subtopic.")
        
        return attrs
    
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source=CREATED_BY_USERNAME)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'post', 'replies','created_by', 'replies']
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj.id)
        return CommentSerializer(replies, many=True, context=self.context).data
    
    def validate(self, attrs):
        if 'parent_comment' not in attrs and 'post' not in attrs:
            raise serializers.ValidationError("Comment must belong to a Post or Comment.")
        
        if 'parent_comment' in attrs and 'post' in attrs:
            raise serializers.ValidationError("Comment cannot belong to both a Post and Comment.")
        
        return attrs
    


