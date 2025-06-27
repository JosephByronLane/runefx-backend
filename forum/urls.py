from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'topics', views.TopicViewSet) #gets all topics

urlpatterns = [
    path('topics/<int:topic_id>/posts/', views.TopicPostCreateView.as_view(), name='topic-posts'), # post
    path('topics/<int:topic_id>/subtopics/', views.TopicSubtopicCreateView.as_view(), name='topic-subtopics'), # post
    path('topics/<int:topic_id>/', views.TopicDetailListView.as_view(), name='topic-detail'), # get

    path('subtopics/<int:subtopic_id>/', views.SubtopicDetailListView.as_view(), name='topic-subtopic-detail'), #get
    path('subtopics/<int:subtopic_id>/posts/', views.SubtopicPostListView.as_view(), name='subtopic-posts'), #post

    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post-detail'), #get
    path('posts/<int:post_id>/comments/', views.PostCommentListView.as_view(), name='post-comments'), #post

    path('', include(router.urls)),
]

