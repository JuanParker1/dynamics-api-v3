"""
Serializers for approvals
"""
import json

from django.utils.translation import gettext as _
from rest_framework import serializers


class ApprovalTypeConfigurationSerializer(serializers.Serializer):
    """
    Configuration for type of approval serializer
    """
    flagged = serializers.ListField(
        label=_('Flagged approvals'),
        help_text=_('List of approval IDS that have been flagged'),
        child=serializers.IntegerField(),
        source='flagedVisa',
        read_only=True
    )
    order = serializers.ListField(
        label=_('Order of the approvals'),
        help_text=_('Order of the approval step IDs'),
        child=serializers.IntegerField(),
        read_only=True,
        source='visasOrder'
    )


class ApprovalTypeSerializer(serializers.Serializer):
    """
    Serializer for a type of approval
    """
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
    configuration = ApprovalTypeConfigurationSerializer(
        label=_('Approval type configuration'),
        help_text=_('Configuration of the approval type'),
        source='content',
        required=False,
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


class ApprovalSerializer(serializers.Serializer):
    """
    Serializer for Approval object (Visa from Kairnial)
    """
    document_id = serializers.IntegerField(
        label=_('ID of the document'),
        help_text=_('Numeric ID of the document'),
        source='entete_id',
        read_only=True
    )
    archived = serializers.BooleanField(
        label=_('Archived'),
        help_text=_('Is approval type archived'),
        source='archive',
        default=False,
        read_only=True
    )
    workflow_id = serializers.IntegerField(
        label=_('ID of the workflow'),
        help_text=_('Numeric ID of the workflow'),
        source='fv_circuit',
        read_only=True
    )
    approval_id = serializers.IntegerField(
        label=_('ID of the approval'),
        help_text=_('Numeric ID of the approval'),
        source='fv_visa',
        read_only=True
    )
    approval_step_id = serializers.IntegerField(
        label=_('ID of the approval step'),
        help_text=_('Numeric ID of the step of the approval'),
        source='fv_subvisa',
        read_only=True
    )
    approval_date = serializers.DateField(
        label=_('Date of the approval step'),
        help_text=_('Date of the approval step'),
        source='fv_date',
        read_only=True
    )
    comment = serializers.CharField(
        label=_('Approval step comment'),
        help_text=_('Comment on the approval step'),
        read_only=True
    )
    title = serializers.CharField(
        label=_('Approval title'),
        help_text=_('Title of the approval'),
        source='titleVisa',
        read_only=True
    )
    number = serializers.IntegerField(
        label=_('Approval number'),
        help_text=_('Approval number'),
        source='numVisa',
        read_only=True
    )
    chrono_number = serializers.IntegerField(
        label=_('Approval chronological number'),
        help_text=_('Approval chronological number'),
        source='numChronoVisa',
        read_only=True
    )
