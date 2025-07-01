from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'all', views.ReleaseViewSet)

urlpatterns = [

    path('single/<int:release_id>/', views.ReleaseDetailView.as_view(), name="release-detail"),

    path('', include(router.urls)),
]