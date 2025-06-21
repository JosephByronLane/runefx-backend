from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from .models import Topic, Subtopic, Post, Comment
from .serializers import TopicSerializer, SubtopicSerializer, PostSerializer, CommentSerializer, TopicSerializerWithoutPosts
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializerWithoutPosts
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Topic.objects.all().order_by('id')

# LIST VIEWS
class TopicPostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['topic'] = self.kwargs['topic_id']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, topic_id=self.kwargs['topic_id'])

class SubtopicPostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        subtopic_id = self.kwargs['subtopic_id']
        return Post.objects.filter(subtopic__id=subtopic_id)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['subtopic'] = self.kwargs['subtopic_id']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, subtopic_id=self.kwargs['subtopic_id'])

class TopicDetailListView(generics.RetrieveAPIView):
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'topic_id'
    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return Topic.objects.filter(id=topic_id)
    
class PostCommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id)
    
    def create(self, request, *args, **kwargs):

        data = request.data.copy()
        data['post'] = self.kwargs['post_id']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, post_id=self.kwargs['post_id'])


class TopicSubtopicCreateView(generics.CreateAPIView):
    serializer_class = SubtopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # we override it since if we call through /topics/<topic_id>/subtopics/ we need to get the topic id
    # since the serializer can't infer it from the request
    def create(self, request, *args, **kwargs):
        data= request.data.copy()
        data['parent_topic'] = self.kwargs['topic_id']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SubtopicDetailListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'subtopic_id'

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()