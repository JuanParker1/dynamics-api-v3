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


class ModuleSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(
        label=_("Module UUID"),
        read_only=True
    )
    route = serializers.CharField(
        label=_('Route of the module'),
        read_only=True
    )
    url = serializers.CharField(
        label=_('URL of the module'),
        read_only=True,
    )
    name = serializers.SerializerMethodField()
    subtitle = serializers.CharField(
        label=_('subtitle of the module'),
        read_only=True,
        source='subTitle'
    )
    icon = serializers.CharField(
        label=_('icon of the module'),
        read_only=True
    )
    target = serializers.CharField(
        label=_('target of the module'),
        read_only=True
    )
    index = serializers.IntegerField(
        label=_('index of the module'),
        read_only=True
    )
    viewable = serializers.BooleanField(
        label=_('is module viewable'),
        read_only=True
    )

    def get_name(self, obj):
        return obj.get('title')
