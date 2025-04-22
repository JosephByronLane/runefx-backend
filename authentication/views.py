from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from rest_framework import permissions
from runefx_backend import settings
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
# Create your views here.
from django.shortcuts import get_object_or_404
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
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response_data = {
            'message' : 'User recieved correctly',
            'user': serializer.data
        }

        return Response(response_data)
    

class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
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
                path=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            )

            response.data['message'] = "Authentication successful"

        
        elif response.status_code == 401:
            # we handle the auth response type as message and user in the frontend
            detail_message = ''
            if response.data['detail']:
                detail_message = response.data['detail']
                del response.data['detail']
            response.data['user'] = {}
            response.data['message'] = detail_message
        
        return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
    def post(self, request, *args, **kwargs):
        #only access to ken is handled in the middleware, refresh tokens need cookie access directly
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        print(refresh_token)
        if not refresh_token:
            return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['refresh'] = refresh_token

        return super().post(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                expires=datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            )

            response.data['message'] = "Token refreshed successfully"

        if response.status_code == 401:
            print(f"NOT AUTHORIZED 401 {response}")

        return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

            if not refresh_token:
                return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

            response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'])
            response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'], path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'])

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)