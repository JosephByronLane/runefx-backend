from .views import RegisterView, UserDetailView, CookieTokenObtainPairView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', TokenVerifyView.as_view(), name='verify-token'),
    path('me/', UserDetailView.as_view(), name='me'), #move to separate user app
]


