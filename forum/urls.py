from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'topics', views.TopicViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('topics/<int:topic_id>/posts/', views.TopicPostListView.as_view(), name='topic-posts'),
    path('topics/<int:topic_id>/subtopics/', views.TopicSubtopicListView.as_view(), name='topic-subtopics'),
    path('topics/<int:topic_id>/subtopics/<int:subtopic_id>/', views.TopicSubtonicDetailListView.as_view(), name='topic-subtopic-detail'),

    path('subtopics/<int:subtopic_id>/posts/', views.SubtopicPostListView.as_view(), name='subtopic-posts'),
    path('posts/<int:post_id>/comments/', views.PostCommentListView.as_view(), name='post-comments'),
]