"""
Project information serializers
"""
import json
import uuid

from django.utils.translation import gettext as _
from rest_framework import serializers

from dynamics_apis.common.serializers import CastingDateField


class ProjectInfoSerializer(serializers.Serializer):
    """
    Serializer for project information
    """
    logo = serializers.CharField(label=_("Project logo"), source='LOGO', read_only=True)
    project_site = serializers.CharField(
        label=_("Project minisite"),
        help_text=_("Project minisite URL"),
        source='minisite',
        required=False, read_only=True)
    pin_statuses_names = serializers.CharField(
        label=_("Names of defect statuses"),
        help_text=_("Names of defect statuses"),
        source='PIN_STATUSES_NAMES',
        required=False, read_only=True)
    photo_1 = serializers.CharField(
        label=_("Project photo 1"),
        help_text=_("First photo of the project"),
        source='PHOTO_OP', required=False,
        read_only=True)
    photo_2 = serializers.CharField(
        label=_("Project photo 2"),
        help_text=_("Second photo of the project"),
        source='PHOTOOP_1', required=False,
        read_only=True)
    photo_3 = serializers.CharField(
        label=_("Project photo 3"),
        help_text=_("Third photo of the project"),
        source='PHOTOOP_2', required=False,
        read_only=True)
    description = serializers.CharField(
        label=_("Project description"),
        help_text=_("Description of the project"),
        source='DESCOP',
        required=False, read_only=True)
    address = serializers.CharField(
        label=_("Project address"),
        help_text=_("Address of the project"),
        required=False,
        read_only=True)
    region = serializers.CharField(
        label=_("Region of the project"),
        help_text=_("Region of the project"),
        required=False, read_only=True)
    city = serializers.CharField(
        label=_("City of the project"),
        help_text=_("City of the project"),
        source='town', required=False,
        read_only=True)
    zone = serializers.CharField(
        label=_("Zone of the project"),
        help_text=_("Zone of the project"),
        required=False, read_only=True)
    type = serializers.CharField(
        label=_("Type of the project"),
        help_text=_("Type of the project from client perspective"),
        required=False, read_only=True)
    picture = serializers.CharField(
        label=_("Picture of the project"),
        help_text=_("Picture of the project"),
        required=False,
        read_only=True)


class ProjectSerializer(serializers.Serializer):
    """
    Serializer for the Kairnial Project response
    """
    id = serializers.CharField(
        label=_("Project ID"),
        help_text=_("Project ID"),
        source='g_nom', read_only=True)
    uuid = serializers.CharField(
        label=_("Project UUID"),
        help_text=_("Project Universal ID"),
        read_only=True)
    name = serializers.CharField(
        label=_("Name of the project"),
        help_text=_("Name of the project"),
        source='g_desc', read_only=True)
    url = serializers.URLField(
        label=_('Project URL'),
        help_text=_('Frontend direct URL to the project'),
        source='frontendURL'
    )
    services_backend = serializers.CharField(
        label=_("Backend serving the project"),
        help_text=_(
            "Karnial has servers in multiple locations, this provides info on the location of the data"),
        source='g_photo', read_only=True)
    authentication_backend = serializers.CharField(
        label=_("Authentication backend serving the project"),
        help_text=_(
            "Karnial has servers in multiple locations, this provides info on the location of the data"),
        source='g_oauth', read_only=True)
    active = serializers.BooleanField(
        label=_("Is project active"),
        help_text=_("Is project active"),
        source='g_running', default=1, read_only=True)
    maintenance = serializers.BooleanField(
        label=_("Is project under maintenance"),
        help_text=_("Is project under maintenance"),
        source='g_maintenance', default=0,
        read_only=True)
    infos = serializers.SerializerMethodField(
        label=_("Additional project information"),
        help_text=_("Additional project information"),
        read_only=True)
    metadata = serializers.CharField(
        label=_("Project metadata"),
        help_text=_("Project metadata"),
        source='g_metadata', required=False, read_only=True)
    application_type = serializers.CharField(
        label=_("Type of application"),
        help_text=_("Type of application hosting the project"),
        source='app_type',
        read_only=True)
    last_activity = serializers.DateTimeField(
        label=_("Date of last activity"),
        help_text=_("Date of last activity on the project"),
        source='lastactivity', read_only=True, format='%Y-%M-%DT%h:%m:%s')
    creation_date = serializers.DateTimeField(
        label=_("Date of creation"),
        help_text=_("Date of project creation"),
        source='g_createdate', format='%Y-%M-%D',
        read_only=True)
    project_type = serializers.CharField(
        label=_("Type of project"),
        help_text=_("Type of project from a Kairnial perspective"),
        source='app_type',
        read_only=True)
    creator = serializers.CharField(
        label=_("Creator of the project"),
        help_text=_("Creator of the project"),
        source='createBy',
        read_only=True)
    base_project = serializers.CharField(
        label=_("Base project"),
        help_text=_("Template used for this project"),
        source='serial',
        read_only=True)

    def get_infos(self, obj):
        return ProjectInfoSerializer(json.loads(obj.get('g_infos'))).data


class ProjectCreationSerializer(serializers.Serializer):
    """
    Serializer to create a new project
    """
    name = serializers.CharField(
        label=_('Project name'),
        help_text=_('Name of the project, max 255 characters'),
        required=True,
        max_length=255
    )
    skip_emails = serializers.BooleanField(
        label=_("Skip email notification"),
        help_text=_("Do not send notification email on project creation"),
        default=False,
        source='noEmail'
    )
    language = serializers.CharField(
        label=_("Project language"),
        help_text=_("Base language for the project"),
        default='en'
    )
    environment = serializers.CharField(
        label=_("Project environment"),
        help_text=_("Base configuration for the project"),
        default='default'
    )
    template = serializers.CharField(
        label=_("Project template UUID"),
        help_text=_("Create project from project template. UUID of the project template"),
        required=False,
        source='type/app_uuid'
    )


class ProjectUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(
        label=_('Project name'),
        help_text=_('Name of the project, max 255 characters'),
        required=True,
        source='g_desc'
    )
    base_project = serializers.CharField(
        label=_('Project serial'),
        help_text=_('Project external code'),
        required=False
    )
    address = serializers.CharField(
        label=_('Project address'),
        help_text=_('Address of the project'),
        required=False
    )
    city = serializers.CharField(
        label=_('Project city'),
        help_text=_('City of the project'),
        required=False
    )
    region = serializers.CharField(
        label=_('Project region'),
        help_text=_('Region of the project'),
        required=False
    )
    zone = serializers.CharField(
        label=_('Project zone'),
        help_text=_('Zone of the project'),
        required=False
    )
    type = serializers.CharField(
        label=_('Project type'),
        help_text=_('Type of the project'),
        required=False
    )


class ProjectIntegrationModuleSerializer(serializers.Serializer):
    module_id = serializers.CharField(
        label=_('Module ID'),
        help_text=_('Text identifier of a module (e.g. rfiles)'),
        source='route',
        read_only=True
    )
    module_name = serializers.CharField(
        label=_('Module name'),
        help_text=_('Name of the module'),
        source='title',
        read_only=True
    )
    module_url = serializers.URLField(
        label=_('Module URL'),
        help_text=_('Module Path'),
        read_only=True,
        source='url'
    )
    module_icon = serializers.CharField(
        label=_('Module icon'),
        help_text=_('URL to the icon of the module'),
        read_only=True,
        source='icon'
    )


class ProjectIntegrationMetadataSerializer(serializers.Serializer):
    project_code = serializers.CharField(
        label=_('Project code'),
        help_text=_('RGOC value'),
        read_only=True
    )
    modules = ProjectIntegrationModuleSerializer(label=_('List of project modules'), many=True)


class ProjectIntegrationSerializer(serializers.Serializer):
    """
    Serializer for CIC/Atrium integration
    """
    project_id = serializers.UUIDField(
        label=_("Project identifier"),
        help_text=_("Project UUID identifier in the product"),
        required=True,
        source='uuid'
    )
    project_name = serializers.CharField(
        label=_('Project name'),
        help_text=_("String representing the project name"),
        required=True,
        source='g_desc'
    )
    start_date = CastingDateField(
        label=_('Project start date'),
        help_text=_("ISO start date of the project"),
        required=True,
        source='g_createdate'
    )
    end_date = CastingDateField(
        label=_('Project end date'),
        help_text=_("ISO start date of the project"),
        source='g_enddate',
        allow_null=True
    )
    source_system = serializers.CharField(
        label=_('Source system'),
        help_text=_('Immutable string'),
        default='Kairnial'
    )
    source_system_id = serializers.UUIDField(
        label=_('Source system ID'),
        help_text=_('ID of the product'),
        default=uuid.uuid4(),
    )
    project_url = serializers.URLField(
        label=_('Project URL'),
        help_text=_('Frontend direct URL to the project'),
        source='frontendURL'
    )
    cover_image_url = serializers.URLField(
        label=_('Project image URL'),
        help_text=_('URL to a PNG image with ratio of 2:1 and at least 600px by 300px '),
        allow_null=True,
        allow_blank=True

    )
    meta_data = ProjectIntegrationMetadataSerializer(
        label=_('Project metadata'),
        help_text=_('Additional info to integration Atrium')
    )
