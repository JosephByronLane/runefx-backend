from django.utils.deprecation import MiddlewareMixin
from runefx_backend import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTCookieMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #if you need the refresh token, you handle it in the view.
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"



        response = self.get_response(request)
        return response