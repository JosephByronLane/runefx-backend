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
        return PostSerializerWithoutReplies(posts, many=True, context=self.context).data


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'created_by','subtopic', 'topic', 'comments','created_by']
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
    
    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'username': obj.created_by.username,
                'user_pfp_url': obj.created_by.profile_picture_url
            }
        return None
class PostSerializerWithoutReplies(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source=CREATED_BY_USERNAME)
    amount_of_comments = serializers.SerializerMethodField()
    latest_comment_data = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'subtopic', 'topic','created_by', 'amount_of_comments','latest_comment_data']
        read_only_fields = ['created_at', 'updated_at', 'creatded_by']
    
    def validate(self, attrs):
        if 'subtopic' not in attrs and 'topic' not in attrs:
            raise serializers.ValidationError("Post must belong to a Topic or Subtopic.")
        
        if 'subtopic' in attrs and 'topic' in attrs:
            raise serializers.ValidationError("Post cannot belong to both a Topic and Subtopic.")
        
        return attrs

    def get_amount_of_comments(self, obj):
        if not Comment.objects.filter(post=obj.id).exists():
            return "0"
        
        return Comment.objects.filter(post=obj.id).count()
    
    def get_latest_comment_data(self, obj):
        if not Comment.objects.filter(post=obj.id).exists():
            return{
                'username': 'Null User',
                'latest_post_time': 0,
                'latest_post_user_pfp': ''
            }   

        post_created_at = Comment.objects.filter(post=obj.id).order_by('-created_at').first().created_at
        post_created_by_pfp = Comment.objects.filter(post=obj.id).order_by('-created_at').first().created_by.profile_picture_url
        post_created_by_username= Comment.objects.filter(post=obj.id).order_by('-created_at').first().created_by.first_name 

        return{
            'username': post_created_by_username,
            'latest_post_time': post_created_at,
            'latest_post_user_pfp': post_created_by_pfp
        }

class SubtopicSerializerWithoutPosts(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    latest_post_data = serializers.SerializerMethodField()
    class Meta:
        model = Subtopic
        fields = ['id', 'title', 'description', 'parent_topic', 'slug', 'latest_post_data', 'post_count']
    
    def validate(self, data):
        if 'parent_topic' not in data :
            raise serializers.ValidationError("Subtopic must belong to a Topic.")
        return data

    def get_post_count(self, obj):
        return Post.objects.filter(subtopic=obj.id).count()
    
    def get_latest_post_data(self, obj):
        if not Post.objects.filter(subtopic=obj.id).exists():
            return{
                'username': 'Null User',
                'latest_post_time': 0,
                'latest_post_user_pfp': ''
            }        
        post_created_at = Post.objects.filter(subtopic=obj.id).order_by('-created_at').first().created_at
        post_created_by_pfp = Post.objects.filter(subtopic=obj.id).order_by('-created_at').first().created_by.profile_picture_url
        post_created_by_username= Post.objects.filter(subtopic=obj.id).order_by('-created_at').first().created_by.first_name 

        return{
            'username': post_created_by_username,
            'latest_post_time': post_created_at,
            'latest_post_user_pfp': post_created_by_pfp
        }
    
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

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
    

    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'username': obj.created_by.username,
                'user_pfp_url': obj.created_by.profile_picture_url
            }
        return None
