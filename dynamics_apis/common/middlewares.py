"""
Kairnial authentication middleware
"""

from django.conf import settings
from django.http import JsonResponse
from jose import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.middleware.security import SecurityMiddleware

KAIRNIAL_AUTH_DOMAIN = settings.KIARNIAL_AUTH_DOMAIN
API_AUDIENCE = settings.KAIRNIAL_AUDIENCE
ALGORITHMS = ["RS256"]

KAIRNIAL_AUTH_PUBLIC_KEY = settings.KAIRNIAL_AUTH_PUBLIC_KEY


class KairnialAuthMiddleware(object):
    """
    Check the jwt token passed by the request
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def jwt_get_username_from_payload_handler(payload):
        username = payload.get('sub').replace('|', '.')
        authenticate(remote_user=username)
        return username

    def __call__(self, request):
        # GET TOKEN
        try:
            request.token = request.META.get('HTTP_AUTHENTICATION').split()[1]
        except (AttributeError, IndexError):
            pass
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        client_id = view_kwargs.get('client_id', None)
        if client_id:
            request.client_id = client_id

