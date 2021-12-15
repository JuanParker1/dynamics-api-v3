"""
Authentication views
"""
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dynamics_apis.common.serializers import ErrorSerializer
from .serializers import PasswordAuthenticationSerializer, APIKeyAuthenticationSerializer, \
    AuthResponseSerializer
from .services import KairnialAuthentication, KairnialAuthenticationError


class PasswordAuthenticationView(APIView):
    """
    Create an authentication token from user/password
    """
    permission_classes = []

    @extend_schema(
        summary=_("Get a token from user / password"),
        description=_("Create token from username / password authentication"),
        request=PasswordAuthenticationSerializer,
        responses={200: AuthResponseSerializer, 400: ErrorSerializer},
        methods=["POST"]
    )
    def post(self, request):
        serializer = PasswordAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            ka = KairnialAuthentication(client_id=serializer.validated_data.get('client_id'))
            try:
                auth_response = ka.password_authentication(
                    username=serializer.validated_data.get('username'),
                    password=serializer.validated_data.get('password'),
                )
                resp_serializer = AuthResponseSerializer(auth_response)
                return Response(resp_serializer.data, status=status.HTTP_200_OK)
            except KairnialAuthenticationError as e:
                return Response(str(e), content_type='application/text',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)


class APIKeyAuthenticationView(APIView):
    """
    Create an authentication token from user/password
    """
    permission_classes = []

    @extend_schema(
        summary=_("Get a token from API key"),
        description=_("Create token from API key / secret authentication"),
        responses={200: AuthResponseSerializer, 400: ErrorSerializer},
        request=APIKeyAuthenticationSerializer,
        methods=["POST"]
    )
    def post(self, request):
        serializer = APIKeyAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            ka = KairnialAuthentication(client_id=serializer.validated_data.get('client_id'))
            try:
                auth_response = ka.secrets_authentication(
                    api_key=serializer.validated_data.get('api_key'),
                    api_secret=serializer.validated_data.get('api_secret'),
                    scopes=serializer.validated_data.get('scopes'),
                )
                resp_serializer = AuthResponseSerializer(auth_response)
                return Response(resp_serializer.data, status=status.HTTP_200_OK)
            except KairnialAuthenticationError as e:
                return Response(str(e), content_type='application/text',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
