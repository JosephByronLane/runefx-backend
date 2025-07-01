from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'blogs', views.ReleaseViewSet)
urlpatterns = [

    path('blogs/<int:blod_id>/', views.ReleaseDetailView.as_view(), name="blog-detail"),

    path('', include(router.urls)),
]