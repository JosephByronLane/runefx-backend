from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from .models import Topic, Subtopic, Post, Comment
from .serializers import TopicSerializer, SubtopicSerializer, PostSerializer, CommentSerializer
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)




# LIST VIEWS

class TopicPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return Post.objects.filter(topic__id=topic_id)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, topic_id=self.kwargs['topic_id'])

class SubtopicPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        subtopic_id = self.kwargs['subtopic_id']
        return Post.objects.filter(subtopic__id=subtopic_id)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, subtopic_id=self.kwargs['subtopic_id'])


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, post_id=self.kwargs['post_id'])


class TopicSubtopicListView(generics.ListCreateAPIView):
    serializer_class = SubtopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return Subtopic.objects.filter(parent_topic_id=topic_id)
    
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

#sounds weird but its the subtopic getter for subtopics
class SubtopicSubtopicListView(generics.ListCreateAPIView):
    serializer_class = SubtopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        subtopic_id = self.kwargs['subtopic_id']
        return Subtopic.objects.filter(subtopic_id=subtopic_id)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, subtopic_id=self.kwargs['subtopic_id'])