from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [

    path('blogs', views.ReleaseViewSet.as_view(), name="all-blogs"),
    path('blogs/<int:blod_id>/', views.ReleaseDetailView.as_view(), name="blog-detail"),

    path('', include(router.urls)),
]