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
        default=False
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
        default=True
    )
    include_updated = serializers.BooleanField(
        label=_('Include updated defects'),
        help_text=_('include updated defects'),
        source='modified',
        default=True
    )
    updated_by_me = serializers.BooleanField(
        label=_('Updated by me'),
        help_text=_('Filter on defects I have updated'),
        source='modifiedbyme',
        default=True
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
    )
    # Weird stuff
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