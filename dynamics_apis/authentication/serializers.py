"""
Authentication serializers
"""
import os

from django.utils.translation import ugettext as _
from rest_framework import serializers


class AuthUserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(label=_("User Unique ID"))
    first_name = serializers.CharField(label=_("User first name"))
    last_name = serializers.CharField(label=_("User last name"))
    full_name = serializers.CharField(label=_("User full name"))
    email = serializers.CharField(label=_("User email"))


class PasswordAuthenticationSerializer(serializers.Serializer):
    """
    Password authentication class
    """
    client_id = serializers.CharField(label=_("Client ID"), default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', _('Type your client ID here')))
    email = serializers.CharField(label=_("User unique identifier"), help_text=_('Type your email here'), default=_('Type your email here'))
    password = serializers.CharField(label=_("Password"), help_text=_('Type your password here'), default=_('Type your password here'))


class APIKeyAuthenticationSerializer(serializers.Serializer):
    """
    API Key / Secret authentication class
    """
    client_id = serializers.CharField(label=_("Client ID"), default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', ''))
    api_key = serializers.CharField(label=_("User API key"), default=os.environ.get('DEFAULT_KAIRNIAL_API_KEY', ''))
    api_secret = serializers.CharField(label=_("User API secret"),  default=os.environ.get('DEFAULT_KAIRNIAL_API_SECRET', ''))


class AuthResponseSerializer(serializers.Serializer):
    """
    Serialize authentication response
    """
    user = AuthUserSerializer()
    token_type = serializers.CharField(label=_("Type of token to pass to the Authorization header"))
    access_token = serializers.CharField(label=_("Access token to use in Authentication header, typically 'Authorization: <token_type> <access_token>. Access tokens for APIs last for 24 hours"))
    expires_in = serializers.IntegerField(label=_("Number of seconds before token exipiration"))
    scope = serializers.CharField(label=_("Functions accessible using this token"))
