"""
Serializers for Kairnial BIM module
"""

from django.utils.translation import gettext as _
from rest_framework import serializers

from dynamics_apis.common.serializers import CastingIntegerField, CastingDateTimeField

class BIMCategoriesSerializer(serializers.Serializer):
    """
    Serializer for a BIM category
    """
    id = serializers.UUIDField(
        label=_('Category ID'),
        help_text=_('UUID of the category'),
        read_only=True
    )
    name = serializers.CharField(
        label=_('Category name'),
        help_text=_('Text name of the category'),
        read_only=True,
        source='label'
    )