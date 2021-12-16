"""
Common serializers
"""
from django.utils.translation import gettext as _
from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    status = serializers.IntegerField(label=_("HTTP error code"))
    code = serializers.IntegerField(label=_("Application error code"), default=0)
    description = serializers.CharField(label=_("Detailed description"))