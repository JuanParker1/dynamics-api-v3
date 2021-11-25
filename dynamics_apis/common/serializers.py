"""
Common serializers
"""
from django.utils.translation import ugettext as _
from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    status = serializers.IntegerField(label=_("HTTP error code"))
    code = serializers.IntegerField(label=_("Application error code"))
    description = serializers.CharField(label=_("Detailed description"))