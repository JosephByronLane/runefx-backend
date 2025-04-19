from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from rest_framework import permissions
from runefx_backend import settings
from datetime import datetime
# Create your views here.

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user
    

class CookieTokenObtainPairView(TokenObtainPairView):
    # url queries api -> request routed to CookieTokenObtainPairView
    # then the parent class TokenObtainPairView answers the request
    # and finally before returning the response it calls finalize_response
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            #access
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                expires=datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            )

            #refresh
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=refresh_token,
                expires=datetime.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            )

            #removing tokens from body, keeping them in there removes the point of having them in the cookies lmao
            if 'refresh' in response.data:
                del response.data['refresh']

            if 'access' in response.data:
                del response.data['access']

            response.data['message'] = "Authentication successful"

            return super().finalize_response(request, response, *args, **kwargs)
