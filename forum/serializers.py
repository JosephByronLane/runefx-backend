from rest_framework import serializers
from django.db.models import Count
from .models import Topic, Subtopic, Post, Comment

CREATED_BY_USERNAME = 'created_by.username'
#for fetching topics without posts and subtopics posts
class TopicSerializerWithoutPosts(serializers.ModelSerializer):
    subtopics = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'subtopics', 'slug']

    def get_subtopics(self, obj):
        subtopics = Subtopic.objects.filter(parent_topic=obj.id)
        return SubtopicSerializerWithoutPosts(subtopics, many=True, context=self.context).data



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
        print("Posts in topic:", posts)
        return PostSerializer(posts, many=True, context=self.context).data


class SubtopicSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    class Meta:
        model = Subtopic
        fields = ['id', 'title', 'description','parent_topic', 'posts', 'slug']
    
    def validate(self, data):
        if 'parent_topic' not in data :
            raise serializers.ValidationError("Subtopic must belong to a Topic.")

        return data
    
    def get_posts(self, obj):
        posts = Post.objects.filter(subtopic=obj.id)
        return PostSerializer(posts, many=True, context=self.context).data


class SubtopicSerializerWithoutPosts(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    latest_post_user = serializers.SerializerMethodField()
    latest_post_time = serializers.SerializerMethodField()
    class Meta:
        model = Subtopic
        fields = ['id', 'title', 'description', 'parent_topic', 'slug', 'post_count', 'latest_post_user', 'latest_post_time']
    
    def validate(self, data):
        if 'parent_topic' not in data :
            raise serializers.ValidationError("Subtopic must belong to a Topic.")
        return data

    def get_post_count(self, obj):
        return Post.objects.filter(subtopic=obj.id).count()
    
    def get_latest_post_user(self, obj):
        if not Post.objects.filter(subtopic=obj.id).exists():
            return None  #only for testing purposes, in production there WILL be posts, so there isn't a need to check for this
        return Post.objects.filter(subtopic=obj.id).order_by('-created_at').first().created_by.username 
    
    def get_latest_post_time(self, obj):
         return Post.objects.filter(subtopic=obj.id).order_by('-created_at').first()


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source=CREATED_BY_USERNAME)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'subtopic', 'topic', 'comments','created_by']
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
        fields = ['id', 'content', 'created_at', 'updated_at', 'post', 'created_by', 'replies']
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def get_replies(self, obj):
        replies = Comment.objects.filter(replies=obj.id)
        return CommentSerializer(replies, many=True, context=self.context).data
    
    def validate(self, attrs):
        if 'post' not in attrs :
            raise serializers.ValidationError("Comment must belong to a Post.")
        
        return attrs
    


