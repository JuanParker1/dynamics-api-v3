"""
Serializers for approvals
"""
from django.utils.translation import gettext as _
from rest_framework import serializers


class ApprovalTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        label=_('Approval type ID'),
        help_text=_('Numeric ID of the approval type'),
        source='noteId',
        read_only=True
    )
    parent_id = serializers.IntegerField(
        label=_('Approval type parent ID'),
        help_text=_('Numeric ID of the parent of the approval type'),
        source='parentId',
        required=False,
        read_only=True
    )
    name = serializers.CharField(
        label=_('Approval type name'),
        help_text=_('Name of the approval type'),
        source='label',
        read_only=True
    )
    content = serializers.CharField(
        label=_('Approval type content'),
        help_text=_('Content of the approval type'),
        source='label',
        read_only=True
    )
    archived = serializers.BooleanField(
        label=_('Archived'),
        help_text=_('Is approval type archived'),
        source='archive',
        default=False,
        read_only=True
    )
    created_at = serializers.DateTimeField(
        label=_('Creation date'),
        help_text=_('Date of creation'),
        source='createdDate',
        read_only=True
    )
    updated_at = serializers.DateTimeField(
        label=_('Update date'),
        help_text=_('Date of modification'),
        source='modifiedDate',
        required=False,
        read_only=True
    )
