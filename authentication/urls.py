from .views import RegisterView, UserDetailView, CookieTokenObtainPairView, CookieTokenRefreshView, CookieTokenLogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    # path('login/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    # path('verify-token/', TokenVerifyView.as_view(), name='verify-token'),
    # path('logout/', CookieTokenLogoutView.as_view(), name='logout'),
    # path('me/', UserDetailView.as_view(), name='me'), #move to separate user app
]


