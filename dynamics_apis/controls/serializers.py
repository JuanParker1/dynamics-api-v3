"""
Serializers for Kairnial Controls module
"""
from django.utils.translation import gettext as _
from rest_framework import serializers

from dynamics_apis.common.serializers import CastingIntegerField, CastingDateTimeField


class ControlQuerySerializer(serializers.Serializer):
    """
    Serializer for control instance query parameters
    """
    archived = serializers.IntegerField(
        label=_('Include archived instances'),
        help_text=_('Include archived instances in result set. 2 includes archived instances.'),
        required=False,
        source='archive'
    )
    created_at = serializers.IntegerField(
        label=_('Creation date'),
        help_text=_('Control instance created at timestamp'),
        required=False,
        source='filter_global_stats_date_creation_date'
    )
    started_at = serializers.IntegerField(
        label=_('Start date'),
        help_text=_('Control instance started at timestamp'),
        required=False,
        source='filter_global_stats_date_start_date'
    )
    ended_at = serializers.IntegerField(
        label=_('End date'),
        help_text=_('Control instance ended at timestamp'),
        required=False,
        source='filter_global_stats_date_end_date'
    )
    updated_at = serializers.IntegerField(
        label=_('Update date'),
        help_text=_('Control instance updated at timestamp'),
        required=False,
        source='filter_global_stats_date_modication_date'
    )
    updated_before = serializers.DateField(
        label=_('Control updated before'),
        help_text=_('Control instance created before included timestamp'),
        required=False,
        source='filter_global_stats_date_less_modification'
    )
    updated_after = serializers.DateField(
        label=_('Control updated after'),
        help_text=_('Control instance updated after included timestamp'),
        required=False,
        source='filter_global_stats_date_greater_modification'
    )
    created_before = serializers.DateField(
        label=_('Control created before'),
        help_text=_('Control instance created before included timestamp'),
        required=False,
        source='filter_global_stats_date_less_creation'
    )
    created_after = serializers.DateField(
        label=_('Control created after'),
        help_text=_('Control instance created after included timestamp'),
        required=False,
        source='filter_global_stats_date_greater_creation'
    )
    started_before = serializers.DateField(
        label=_('Control created before'),
        help_text=_('Control instance ended before included timestamp'),
        required=False,
        source='filter_global_stats_date_less_start'
    )
    started_after = serializers.DateField(
        label=_('Control created after'),
        help_text=_('Control instance started after included timestamp'),
        required=False,
        source='filter_global_stats_date_greater_start'
    )
    ended_before = serializers.DateField(
        label=_('Control ended before'),
        help_text=_('Control instance ended before included timestamp'),
        required=False,
        source='filter_global_stats_date_less_end'
    )
    ended_after = serializers.DateField(
        label=_('Control ended after'),
        help_text=_('Control instance ended after included timestamp'),
        required=False,
        source='filter_global_stats_date_greater_end'
    )
    numbers = serializers.ListSerializer(
        label=_('Filter by form number'),
        help_text=_('List of control instance numbers'),
        child=serializers.IntegerField(),
        required=False,
        source='formNumber'
    )
    statuses = serializers.ListSerializer(
        label=_('Filter by list of statuses'),
        help_text=_('List of control instances with status in list'),
        child=serializers.IntegerField(),
        required=False,
        source='filterFormColors'
    )
    users = serializers.ListSerializer(
        label=_('Filter by list of users'),
        help_text=_('List of control instances with user numeric id in list'),
        child=serializers.IntegerField(),
        required=False
    )
    buildings = serializers.ListSerializer(
        label=_('Filter by list of buildings'),
        help_text=_('List of control instances with building numeric id in list'),
        child=serializers.IntegerField(),
        required=False
    )
    levels = serializers.ListSerializer(
        label=_('Filter by list of levels'),
        help_text=_('List of control instances with level numeric id in list'),
        child=serializers.IntegerField(),
        required=False
    )
    plan_id = serializers.UUIDField(
        label=_('Filter by plan UUID'),
        help_text=_('Filter by plan UUID'),
        required=False,
        source='planUuid'
    )
    public = serializers.BooleanField(
        label=_('Public instances'),
        help_text=_('Filter on public control instances'),
        required=False
    )


class ControlTemplateQuerySerializer(serializers.Serializer):
    """
    Serializer for ControlTemplate filters
    """
    archived = serializers.IntegerField(
        label=_('Include archived templates'),
        help_text=_('Include archived templates in result set'),
        required=False,
        source='archive'
    )
    id = serializers.IntegerField(
        label=_('Template ID'),
        help_text=_('Filter on template numeric ID'),
        required=False,
        source='templateId'
    )
    uuids = serializers.ListSerializer(
        label=_('Template UUIDs'),
        help_text=_('List of template UUIDs'),
        required=False,
        child=serializers.UUIDField(label=_('Template UUID')),
        source='templateUuidList'
    )
    plan_id = serializers.UUIDField(
        label=_('Plan ID'),
        help_text=_('Unique ID of a plan'),
        required=False,
        source='planUuid'
    )
    tags = serializers.ListSerializer(
        label=_('Tag UUIDs'),
        help_text=_('Filter by list of tag UUIDs'),
        required=False,
        child=serializers.UUIDField()
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
        allow_null=True,
        read_only=True
    )
    id = CastingIntegerField(
        label=_("Control template numeric ID"),
        help_text=_("Numeric ID of the control template"),
        allow_null=True,
        read_only=True
    )
    title = serializers.CharField(
        label=_('Control template title'),
        help_text=_('String title of the control template'),
        required=False
    )
    parent_id = serializers.IntegerField(
        label=_('parent ID'),
        help_text=_('ID of the parent template'),
        required=False
    )
    created_at = CastingDateTimeField(
        label=_('Creation date'),
        help_text=_('Creation timestamp'),
        source='createDate',
        required=True
    )
    updated_at = CastingDateTimeField(
        label=_('Update date'),
        help_text=_('Update timestamp'),
        source='updateDate',
        required=True
    )
    created_by = serializers.CharField(
        label=_('Creator'),
        help_text=_('e-mail of the creator'),
        source='email',
        allow_null=True,
        read_only=True
    )
    category = serializers.CharField(
        label=_('Category label'),
        help_text=_('Label of the category'),
        source='category_label',
        required=False
    )


class ControlInstanceContentValueSerializer(serializers.Serializer):
    """
    Serialize instance content
    """
    position = serializers.IntegerField(
        label=_('Position of the element'),
        help_text=_('numeric value'),
        read_only=True
    )
    input_date = CastingDateTimeField(
        label=_('Input date'),
        help_text=_('Date of the user input'),
        source='date',
        read_only=True
    )
    value = serializers.CharField(
        label=_('Value'),
        help_text=_('Value'),
        allow_null=True,
        allow_blank=True,
        read_only=True
    )


class ControlInstanceAdditionalInfo(serializers.Serializer):
    """
    Serialize the additional info of a control instance content
    """
    bim_element = serializers.JSONField(
        label=_('BIM element'),
        help_text=_('BIM element characteristics'),
        source='bimElement',

        read_only=True
    )
    bim_model_id = serializers.IntegerField(
        label=_('BIM Model ID'),
        help_text=_('Numeric ID of the BIM model'),
        source='bimModelId',
        read_only=True
    )
    bim_layer_id = serializers.IntegerField(
        label=_('BIM Layer ID'),
        help_text=_('Numeric ID of the BIM layer'),
        source='bimLayerId',
        read_only=True
    )


class ControlInstanceSerializer(serializers.Serializer):
    """
    Serializer for ControlInstance
    """
    uuid = serializers.UUIDField(
        label=_("Control instance UUID"),
        help_text=_("Unique ID of the control insance"),
        required=False
    )
    id = serializers.IntegerField(
        label=_("Control instance ID"),
        help_text=_("Numeric ID of the control instance"),
        source='notes_id',
        required=False
    )
    template_uuid = serializers.UUIDField(
        label=_("Control template UUID"),
        help_text=_("Unique ID of the control template"),
        required=False
    )
    template_id = serializers.IntegerField(
        label=_("Control template ID"),
        help_text=_("Numeric ID of the control template"),
        required=False
    )
    element_uuid = serializers.UUIDField(
        label=_('Element UUID'),
        help_text=_('UUID of the element in the template content'),
        read_only=True
    )
    title = serializers.CharField(
        label=_('Instance title'),
        help_text=_('Title of the instance'),
        required=False
    )
    status = serializers.IntegerField(
        label=_('Status'),
        help_text=_('Numeric value of the status.'),  # TODO: find possible statuses and meanings,
        default=0,
        read_only=True
    )
    created_by = serializers.IntegerField(
        label=_('Creator ID'),
        help_text=_('Numeric ID of the creator'),
        read_only=True
    )
    position = serializers.CharField(
        label=_('Position'),
        help_text=_('Position of the value'),
        read_only=True
    )
    created_at = CastingDateTimeField(
        label=_('Date of creation'),
        help_text=_('Date the instance was created'),
        source='creation date',
        read_only=True
    )
    updated_at = CastingDateTimeField(
        label=_('Date of modification'),
        help_text=_('Date the instance was modified'),
        source='modification_date',
        read_only=True
    )
    map_category_name = serializers.CharField(
        label=_('Map category name'),
        help_text=_('Name of the category of the map'),
        read_only=True
    )
    map_name = serializers.CharField(
        label=_('Map name'),
        help_text=_('Name of the map'),
        read_only=True
    )
    plan_uuid = serializers.UUIDField(
        label=_('UUID of the plan'),
        help_text=_('Optionnal link to a plan'),
        read_only=True,
    )
    additional_info = ControlInstanceAdditionalInfo(
        label=_('Instance additional information'),
        help_text=_('Info relative to the instance content'),
        read_only=True
    )
    values = ControlInstanceContentValueSerializer(
        label=_('Instance values'),
        help_text=_('Values of the instance as text'),
        many=True,
        read_only=True
    )


