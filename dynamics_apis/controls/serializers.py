"""
Serializers for Kairnial Controls module
"""

from django.utils.translation import gettext as _
from rest_framework import serializers
from dynamics_apis.common.serializers import CastingIntegerField


class ControlQuerySerializer(serializers.Serializer):
    """
    Serializer for folder query parameters
    """
    id = serializers.UUIDField(
        label=_("filter on ID"),
        help_text=_("retrieve control with given ID"),
        source='template_uuid',
        required=False
    )
    updated_before = serializers.DateField(
        label=_('folder updated before'),
        help_text=_('date of latest modification'),
        required=False,
        source='modification_end'
    )
    updated_after = serializers.DateField(
        label=_('folder updated after'),
        help_text=_('date of oldest modification'),
        required=False,
        source='modification_start'
    )
    created_before = serializers.DateField(
        label=_('folder created before'),
        help_text=_('date of latest creation'),
        required=False,
        source='creation_end'
    )
    created_after = serializers.DateField(
        label=_('folder created after'),
        help_text=_('date of oldest creation'),
        required=False,
        source='creation_start'
    )


class ControlTemplateElementSerializer(serializers.Serializer):
    """
    Serializer for template element
    """
    key = serializers.CharField(
        label=_('Element key'),
        help_text=_('Element key'),
        required=False
    )
    name = serializers.CharField(
        label=_('Element name'),
        help_text=_('Element name'),
        required=True
    )
    type = serializers.CharField(
        label=_('Element type'),
        help_text=_('Element type'),
        required=True
    )
    type = serializers.CharField(
        label=_('Element color'),
        help_text=_('color name'),
        required=False
    )
    default_value = serializers.CharField(
        label=_('Element color'),
        help_text=_('color name'),
        required=False
    )
    required = serializers.CharField(
        label=_('Is field required'),
        help_text=_('It should be a boolean, pass 0 or 1'),
        default=''
    )
    index = CastingIntegerField(
        label=_('Element index'),
        help_text=_('Position of the element in the list as integer'),
        default=0,
        allow_null=True,
        read_only=True
    )
    choices = serializers.CharField(
        label=_('list of choices'),
        help_text=_('List of comma separated values'),
        required=False
    )
    parent_id = CastingIntegerField(
        label=_('Parent element ID'),
        help_text=_('Numeric ID of the parent element'),
        allow_null=True,
        read_only=True,
        source='parentId'
    )
    settings = serializers.JSONField(
        label=_('JSON settings'),
        help_text=_('Json field for additional settings'),
        read_only=True,
    )


class ControlTemplateContentSettingSerializer(serializers.Serializer):
    """
    Serializer for Control template content settings
    """
    can_create_instances = serializers.BooleanField(
        label=_('Can create instance'),
        help_text=_('Can the current user create instances of thi template'),
        source='canCreateInstances',
        read_only=True,
        default=False
    )
    colorize_section = serializers.BooleanField(
        label=_('Colorize sections'),
        help_text=_('Apply colors on sections to enhance visibility'),
        source='colorizeSections',
        default=False
    )
    hide_states = serializers.BooleanField(
        label=_('Hide states'),
        help_text=_('Boolean flag'),
        source='hideStates',
        read_only=True
    )
    allow_linked_pins = serializers.BooleanField(
        label=_('Allow pins to be linked to instance'),
        help_text=_('Allow pins to be linked to instance'),
        source='allowLinkedPins',
        read_only=True
    )


class ControlTemplateContentSerializer(serializers.Serializer):
    """
    Content of the Control template
    """
    show_columns_only = serializers.BooleanField(
        label=_('Only display columns'),
        help_text=_('Do not show values'),
        default=False,
        source='showOnlyCols'
    )
    groups = serializers.ListSerializer(
        label=_('Group IDs'),
        help_text=_('List of numeric IDs of groups accessing the template content'),
        default=[],
        child=CastingIntegerField()
    )
    elements = ControlTemplateElementSerializer(
        label=_('Control form elements'),
        help_text=_('List of ControlTemplateElements'),
        many=True,
        read_only=True
    )
    settings = ControlTemplateContentSettingSerializer(
        label=_('Template settings'),
        help_text=_('Settings object'),
        required=False,
        read_only=True
    )


class ControlTemplateSerializer(serializers.Serializer):
    """
    Serializer for ControlTemplate
    """
    uuid = serializers.UUIDField(
        label=_("Control template unique ID"),
        help_text=_("UUID of the control template"),
        source='template_uuid',
        allow_null=True,
        read_only=True
    )
    id = CastingIntegerField(
        label=_("Control template numeric ID"),
        help_text=_("Numeric ID of the control template"),
        source='notes_id',
        allow_null=True,
        read_only=True
    ),
    title = serializers.CharField(
        label=_('Control template title'),
        help_text=_('String title of the control template'),
        required=False
    )
    created_at = serializers.DateField(
        label=_('Creation date'),
        help_text=_('Creation timestamp'),
        source='creation_date',
        required=True
    )
    updated_at = serializers.DateField(
        label=_('Update date'),
        help_text=_('Update timestamp'),
        source='creation_date',
        required=True
    )
    created_by = CastingIntegerField(
        label=_('Creator'),
        help_text=_('Numeric ID of the creator'),
        source='creator_id',
        allow_null=True,
        read_only=True
    )
    created_by_email = serializers.CharField(
        label=_('Creator email'),
        help_text=_('e-mail of creator'),
        source='creator_email'
    )
    category = serializers.CharField(
        label=_('Category label'),
        help_text=_('Label of the category'),
        source='category_label',
        required=False
    )


class ControlInstanceSerializer(serializers.Serializer):
    """
    Serializer for ControlInstance
    """
    id = serializers.UUIDField(
        label=_("Control instance ID"),
        help_text=_("UUID of the control instance"),
        source='template_uuid',
        required=False
    )
