"""
Serializers for Kairnial Files module
"""
from django.utils.translation import gettext as _
from rest_framework import serializers


class FolderQuerySerializer(serializers.Serializer):
    """
    Serializer for folder query parameters
    """
    id = serializers.CharField(
        label=_("filter on ID"),
        help_text=_("retrieve folders with given ID"),
        required=False,
        default=False
    )
    all = serializers.BooleanField(
        label=_("retrieve all folders"),
        help_text=_("Retrieve folders from all levels"),
        required=False,
        default=False
    )
    acl = serializers.BooleanField(
        label=_("filter on user authorizations"),
        help_text=_("Retrieve folders that have authorizations on this user"),
        required=False,
        default=False
    )
    updated_before = serializers.DateTimeField(
        label=_('folder updated before'),
        help_text=_('date of latest modification'),
        required=False,
        source='modification_end'
    )
    updated_after = serializers.DateTimeField(
        label=_('folder updated after'),
        help_text=_('date of oldest modification'),
        required=False,
        source='modification_start'
    )
    created_before = serializers.DateTimeField(
        label=_('folder created before'),
        help_text=_('date of latest creation'),
        required=False,
        source='creation_end'
    )
    created_after = serializers.DateTimeField(
        label=_('folder created after'),
        help_text=_('date of oldest creation'),
        required=False,
        source='creation_start'
    )
