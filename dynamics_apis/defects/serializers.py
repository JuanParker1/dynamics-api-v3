"""
Serializers for Kairnial Defects module
"""

from django.utils.translation import gettext as _
from rest_framework import serializers

from dynamics_apis.common.serializers import CastingIntegerField, CastingDateTimeField


class DefectQuerySerializer(serializers.Serializer):
    """
    Serializer for defect query parameters
    """
    id = serializers.UUIDField(
        label=_("filter on ID"),
        help_text=_("retrieve defect with given numeric ID"),
        source='uuidFilter',
        required=False
    )
    description = serializers.UUIDField(
        label=_("filter on description"),
        help_text=_("filter defects containing description, case insensitive"),
        required=False
    )
    search = serializers.CharField(
        label=_("Search on defects"),
        help_text=_("Global search field"),
        required=False
    )
    zone = serializers.CharField(
        label=_("filter on zone"),
        help_text=_("filter defects on zone"),
        required=False
    )
    status = serializers.ListSerializer(
        label=_('List of states'),
        help_text=_('List of defect numeric states'),
        child=serializers.IntegerField(),
        source='filtre',
        required=False
    )
    phases = serializers.ListSerializer(
        label=_('List of project phases'),
        help_text=_('List of phase numeric IDs'),
        child=serializers.IntegerField(),
        source='campagne',
        required=False
    )
    created_by = serializers.ListSerializer(
        label=_('List of creators'),
        help_text=_('List of user numeric IDs'),
        child=serializers.IntegerField(),
        required=False
    )
    main_area = serializers.BooleanField(
        label=_('Main area'),
        help_text=_('Filter on main area, use in conjunction with area_uuids'),
        source='mainPrimaryArea',
        required=False
    )
    area_uuids = serializers.ListSerializer(
        label=_('List of areas'),
        help_text=_('List of area UUIDs'),
        child=serializers.UUIDField(),
        source='areasUuids',
        required=False
    )
    # map_categories = serializers.ListSerializer(
    #     label=_('List of map categories'),
    #     help_text=_('List of map categories numeric IDs'),
    #     child=serializers.IntegerField(),
    #     source='mapCategories',
    #     required=False
    # )
    # maps = serializers.ListSerializer(
    #     label=_('List of maps'),
    #     help_text=_('List of map numeric IDs'),
    #     child=serializers.IntegerField(),
    #     required=False
    # )
    ids = serializers.ListSerializer(
        label=_('List of defect IDs'),
        help_text=_('List of defect numeric IDs'),
        child=serializers.IntegerField(),
        source='filtreid',
        required=False
    )
    note = serializers.CharField(
        label=_('Note'),
        help_text=_('Filter on note'),
        source='impoT',
        required=False
    )
    companies = serializers.ListSerializer(
        label=_('List of company IDs'),
        help_text=_('List of company numeric IDs'),
        child=serializers.IntegerField(),
        source='entreprises',
        required=False
    )
    positions = serializers.ListSerializer(
        label=_('List of company IDs'),
        help_text=_('List of company numeric IDs'),
        child=serializers.CharField(),
        source='entreprises',
        required=False
    )
    company = serializers.CharField(
        label=_('Company ID'),
        help_text=_('Filter on company'),
        source='EntrepriseID',
        required=False
    )
    created_after = serializers.DateField(
        label=_('Defects created after'),
        help_text=_('Included lower bound'),
        source='minimumCreationDate',
        required=False
    )
    created_before = serializers.DateField(
        label=_('Defects created before'),
        help_text=_('Included upper bound'),
        source='maximumCreationDate',
        required=False
    )
    has_attachment = serializers.BooleanField(
        label=_('Defects with attachments '),
        help_text=_('Filter defects with attachments'),
        source='justPhoto',
        required=False
    )
    include_created = serializers.BooleanField(
        label=_('Include created defects'),
        help_text=_('include created defects'),
        source='created',
        required=False
    )
    include_updated = serializers.BooleanField(
        label=_('Include updated defects'),
        help_text=_('include updated defects'),
        source='modified',
        required=False
    )
    updated_by_me = serializers.BooleanField(
        label=_('Updated by me'),
        help_text=_('Filter on defects I have updated'),
        source='modifiedbyme',
        required=False
    )


class DefectSerializer(serializers.Serializer):
    """
    Serializer for defect object
    """
    uuid = serializers.UUIDField(
        label=_('Defect ID'),
        help_text=_('UUID of a defect'),
        read_only=True
    )
    id = serializers.IntegerField(
        label=_('Defect Numeric ID'),
        help_text=_('Numeric ID of the defect'),
        source='note',
        read_only=True
    )
    number = serializers.IntegerField(
        label=_('Defect increment'),
        help_text=_('Numeric incrementof a defect number'),
        source='numero',
        read_only=True
    )
    planview = serializers.CharField(
        label=_('Plan'),
        help_text=_('Identifier of the plan view'),
        source='niveau',
        read_only=True
    )
    description = serializers.CharField(
        label=_('Defect description'),
        help_text=_('Text field for defect description'),
        read_only=True
    )
    active = serializers.BooleanField(
        label=_('Active defect'),
        help_text=_('Is defect active'),
        source='actif',
        default=True,
        read_only=True
    )
    has_comment = CastingIntegerField(
        label=_('Defect has comment'),
        help_text=_('Number of defect comments'),
        source='hasComment',
        read_only=True
    )
    photo = serializers.CharField(
        label=_("Attachments"),
        help_text=_('if no attachment is associated, value is noPhoto, otherwise it contains the number of attachments'),
        read_only=True,
        default='noPhoto'
    )
    # dates
    end_date = CastingDateTimeField(
        label=_('End date'),
        help_text=_('Date of defect closing'),
        source='datef',
        read_only=True
    )
    expected_date = CastingDateTimeField(
        label=_('Expected at'),
        help_text=_('Date tho defect should be closed'),
        source='dateesp',
        read_only=True
    )
    date = CastingDateTimeField(
        label=_('Input date'),
        help_text=_('Date of user input'),
        read_only=True
    )
    # Location
    building = serializers.CharField(
        label=_('Building information'),
        help_text=_('Name of building or location'),
        source='bat',
        read_only=True
    )
    zone = serializers.CharField(
        label=_('Zone'),
        help_text=_('Defect zoning information'),
        read_only=True
    )
    place = serializers.CharField(
        label=_('Place'),
        help_text=_('Defect placement'),
        read_only=True
    )
    coordinates = serializers.CharField(
        label=_('Coordinates'),
        help_text=_('Defect coordinates'),
        source='coord',
        read_only=True
    )
    coordinates_2 = serializers.CharField(
        label=_('Other coordinates'),
        help_text=_('Defect other coordinates'),
        source='coord2',
        read_only=True
    )
    abs_coordinates = serializers.CharField(
        label=_('Absolute coordinates'),
        help_text=_('Defect absolute coordinates'),
        source='abscoord',
        read_only=True
    )
    #
    created_by = serializers.CharField(
        label=_('Created by'),
        help_text=_('Defect rceator information'),
        source='saisipar',
        read_only=True
    )
    company = serializers.CharField(
        label=_('Assigned company'),
        help_text=_('Name of the assigned company'),
        source="entreprise"
    )
    flags = serializers.CharField(
        label=_('Defect flags'),
        help_text=_("Cannot help here..."), # TODO: What is it for ?
        source='falgs'
    ) # Weird stuff
    session = serializers.CharField(
        label=_('On site session'),
        help_text=_('Visit session information'),
        source='pv',
        read_only=True
    )  # session
    previous_text = serializers.CharField(
        label=_('Last modified description'),
        help_text=_('Defect description before last modification'),
        source='ancientexte',
        read_only=True
    )
    modification_type = CastingIntegerField(
        label=_('Modification type'),
        help_text=_('Type of defect modification'),
        read_only=True
    )
    #
    server_time = CastingDateTimeField(
        label=_('Server creation time'),
        help_text=_('Time of creation of creation of the defect on the server'),
        source='serverTime',
        read_only=True
    )
    is_from_server = serializers.BooleanField(
        label=_('Created on server'),
        help_text=_('Defect has been created on server'),
        source='fromServeur',
        read_only=True
    )

class DefectCreateSerializer(serializers.Serializer):
    """
    Serializer for defect input
    """
    id = serializers.UUIDField(
        label=_('Defect universal ID'),
        help_text=_('UUID of the defect'),
        source='guid'
    )
    gpc = serializers.BooleanField(
        label=_('Garantee of perfect completion'),
        help_text=_('Does this defect concern GPC'),
        source='gpa'
    )
    coordinates = serializers.CharField( # TODO: Describe the field structure
        label=_('Defect coordinates'),
        help_text=_(''),
        source='coord'
    )
    coordinates_2 = serializers.CharField( # TODO: Describe the field structure
        label=_('Other defect coordinates'),
        help_text=_(''),
        source='coord2'
    )
    coordinates_3D = serializers.CharField( # TODO: Describe the field structure
        label=_('Defect 3D coordinates'),
        help_text=_('Defect coordinates in a 3D model'),
        source='coord3d'
    )
    campaign_id = serializers.IntegerField(
        label=_('Campaign ID'),
        help_text=_('Numeric ID of a campaign'),
        source='campagne'
    )
    input_date = CastingDateTimeField(
        label=_('Time of input'),
        help_text=_('Datetime of defect input'),
        source='datec'
    )
    building = serializers.CharField(
        label=_('Building location'),
        help_text=_('Text building of the defect'),
        source='bat'
    )
    floor = serializers.CharField(
        label=_('Floor location'),
        help_text=_('Text floor of the defect'),
        source='niveau'
    )
    location = serializers.CharField(
        label=_('Location'),
        help_text=_('Text location of the defect'),
        source='lieu'
    )
    zone = serializers.CharField(
        label=_('Zone'),
        help_text=_('Text zone of the defect'),
    )
    layer_id = serializers.IntegerField(
        label=_('Layer ID'),
        help_text=_('Numeric ID of the layer of the defect'),
        source='couche'
    )
    model_id = serializers.IntegerField(
        label=_('Model ID'),
        help_text=_('Numeric ID of the model of the defect'),
    )
    bim_model_id = serializers.CharField(
        label=_('BIM Map ID'),
        help_text=_('UUID of the BIM model of the defect'),
        source='plan_uuid'
    )
    description = serializers.CharField(
        label=_('Description'),
        help_text=_('Text description of the defect'),
        source='desc'
    )
    end_date = CastingDateTimeField(
        label=_('End date'),
        help_text=_('Datetime of end of defect'),
        source='datef'
    )
    due_date = CastingDateTimeField(
        label=_('Due date'),
        help_text=_('Datetime of due completion of defect'),
        source='datepf'
    )
    expected_date = CastingDateTimeField(
        label=_('Due date'),
        help_text=_('Datetime of due completion of defect'),
        source='dateesp'
    )
    completion_date = CastingDateTimeField(
        label=_('Completion date'),
        help_text=_('Datetime of completion of defect'),
        source='dater'
    )
    additional_date_1 = CastingDateTimeField(
        label=_('Additional date 1'),
        help_text=_('Datetime for additional date'),
        source='date1'
    )
    additional_date_2 = CastingDateTimeField(
        label=_('Additional date 2'),
        help_text=_('Datetime for additional date'),
        source='date2'
    )
    additional_date_3 = CastingDateTimeField(
        label=_('Additional date 3'),
        help_text=_('Datetime for additional date'),
        source='date3'
    )
    status_id = serializers.IntegerField(
        label=_('Status ID'),
        help_text=_('Numeric ID of the status'),
        source='actif'
    )
    photo = serializers.CharField(
        label=_('Defect photo'),
        help_text=_('Text info on the picture of the defect'),
    )
    photo_2 = serializers.CharField(
        label=_('Defect photo'),
        help_text=_('Text info on the picture of the defect'),
        source='photo2'
    )
    photos = serializers.CharField(
        label=_('Defect photos'),
        help_text=_('Field containing information on defect photos'), # TODO: How is this field structured ?
    )
    location_detail_images = serializers.CharField(
        label=_('Defect location images'),
        help_text=_('Field containing information on defect location images'), # TODO: How is this field structured ?
    )
    emitter = serializers.CharField(
        label=_('Emmiter'),
        help_text=_('Name of the emitter'),
        source='saisipar'
    )
    flags = serializers.CharField(
        label=_('Internal flags'),
        help_text=_('Undocumented defect flags'),
    )
    previous_description = serializers.CharField(
        label=_('Previous description'),
        help_text=_('Previous description of the defect'),
        source='anctexte'
    )
    number = serializers.IntegerField(
        label=_('Number'),
        help_text=_('User defined defect number'),
        source='idInt'
    )
    session_id = serializers.CharField(
        label=_('Defect input session ID'),
        help_text=_('On site defect management session ID'),
        source='pv'
    )
    localized_description = serializers.CharField(
        label=_('Localized description'),
        help_text=_('Text for a localized description'), # TODO: Localized or localisation ?
        source='localizedDescription'
    )
    additional_info = serializers.CharField(
        label=_('Additional info'),
        help_text=_('Free text additional information'),
        source='additionalInfos'
    )
    additional_values = serializers.CharField(
        label=_('Additional values'),
        help_text=_('How is that supposed to be structured ?'), # TODO: Identify field structure
        source='supplementaryValues'
    )

class DefectUpdateSerializer(serializers.Serializer):
    """
    Serializer for defect patch
    """
    coordinates = serializers.CharField(  # TODO: Describe the field structure
        label=_('Defect coordinates'),
        help_text=_(''),
        source='coord'
    )
    emitter = serializers.CharField(
        label=_('Defect emitter'),
        help_text=_('Emitter of the defect'),
    )
    description = serializers.CharField(
        label=_('Defect description'),
        help_text=_('Defect description text'),
    )



class DefectAreaSerializer(serializers.Serializer):
    """
    Serializer for an area
    """
    id = serializers.UUIDField(
        label=_('Area ID'),
        help_text=_('UUID of the area'),
        source='uuid',
        read_only=True
    )
    name = serializers.CharField(
        label=_('Area name'),
        help_text=_('Text name of the area'),
        read_only=True
    )
    header = serializers.BooleanField(
        label=_('Aggregated area'),
        help_text=_('Is this area an aggregate'),
        read_only=True
    )
    plan_id = serializers.UUIDField(
        label=_('Plan ID'),
        help_text=_('UUID of the plan'),
        source='plan_uuid',
        read_only=True
    )
    defects_count = serializers.ListSerializer(
        label=_('Number of defects'),
        help_text=_('List of numbers of defects'),
        child=serializers.IntegerField(),
        source='pins',
        read_only = True
    )

class DefectBIMCategorySerializer(serializers.Serializer):
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

class DefectBIMLevelSerializer(serializers.Serializer):
    """
    Serializer for a BIM category
    """
    name = serializers.CharField(
        label=_('Level name'),
        help_text=_('Text name of the level'),
        read_only=True,
        source='label'
    )

