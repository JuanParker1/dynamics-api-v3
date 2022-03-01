"""
Common serializers
"""
from datetime import datetime

from django.utils.translation import gettext as _
from rest_framework import serializers


class CastingIntegerField(serializers.IntegerField):

    def to_representation(self, value):
        if not value:
            value = 0
        return super().to_representation(value)


class CastingDateTimeField(serializers.DateTimeField):

    def to_representation(self, value):
        try:
            value = datetime.fromtimestamp(int(value))
        except (TypeError, ValueError):
            pass
        return super().to_representation(value=value)


class CastingDateField(serializers.DateTimeField):

    def to_representation(self, value):
        try:
            value = datetime.fromtimestamp(int(value)).date()
        except (TypeError, ValueError):
            pass
        return super().to_representation(value=value)


class ErrorSerializer(serializers.Serializer):
    status = serializers.IntegerField(label=_("HTTP error code"))
    code = serializers.IntegerField(label=_("Application error code"), default=0)
    description = serializers.CharField(label=_("Detailed description"))
