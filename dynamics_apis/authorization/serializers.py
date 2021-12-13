"""
Serializers for authorization objects (ACL)
"""
from django.utils.translation import gettext as _
from rest_framework import serializers


class ACLSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(
        label=_("ACL UUID"),
        read_only=True,
        source='item_uuid'
    )
    type = serializers.CharField(
        label=_('ACL type'),
        read_only=True,
        source='item_type'
    )
    acl_type = serializers.CharField(
        label=_('Type of ACL'),
        read_only=True,
    )
    description = serializers.CharField(
        label=_('description of the ACL'),
        read_only=True
    )


class ACLQuerySerializer(serializers.Serializer):
    """
    Serializer for ACL query parameters
    """
    domain = serializers.CharField(
        label=_('ACL domain'),
        help_text=_("Domain of the ACL (bim, dms, ...)"),
        required=False
    )
    search = serializers.CharField(
        label=_('Search in ACL'),
        help_text=_("Search in ACL type and description"),
        required=False
    )