"""
Serializers for Kairnial Files module
"""
import json

from django.utils.translation import gettext as _
from rest_framework import serializers


class FolderQuerySerializer(serializers.Serializer):
    """
    Serializer for folder query parameters
    """
    id = serializers.IntegerField(
        label=_("filter on ID"),
        help_text=_("retrieve folders with given ID"),
        required=False
    )
    all = serializers.BooleanField(
        label=_("retrieve all folders"),
        help_text=_("Retrieve folders from all levels"),
        required=False,
        default=False
    )
    path = serializers.CharField(
        label=_('Folder path'),
        help_text=_('Filter on folders in a given path'),
        required=False
    )
    acl = serializers.BooleanField(
        label=_("filter on user authorizations"),
        help_text=_("Retrieve folders that have authorizations on this user"),
        required=False,
        default=False
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


class FolderInfoSerializer(serializers.Serializer):
    """
    Serializer for folder info
    """
    allowed_extensions = serializers.CharField(
        label=_('Allowed extensions'),
        help_text=_('Comma separeated file extensions allowed in this folder'),
        source='allowed_ext',
        allow_blank=True,
        required=False,
        default=""
    )
    disabled_extensions = serializers.CharField(
        label=_('Disabled extensions'),
        help_text=_('Comma separated file extensions allowed in this folder'),
        source='disabled_ext',
        allow_blank=True,
        required=False,
        default=""
    )
    maximum_size = serializers.CharField(
        label=_('Maximum size allowed'),
        help_text=_('Maximum size allowed in this folder'),
        default="",
        allow_blank=True,
        required=False,
    )
    download_without_index = serializers.BooleanField(
        label=_('Download without index'),
        help_text=_('Do not include index in file name'),
        default=False,
        source='downloadWithoutIndex'
    )
    force_name = serializers.BooleanField(
        label=_('Force name on download'),
        help_text=_('Force upload nam on dowonload'),
        default=False,
        source='forceName'
    )
    naming_convention = serializers.CharField(
        label=_('Naming convention ID'),
        help_text=_('ID of the naming convention'),
        source='nomenclaturesId',
        default="",
        allow_blank=True,
        required=False,
    )
    workflow = serializers.CharField(
        label=_('workflow ID'),
        help_text=_('ID of the workflow'),
        source='circuit',
        default="",
        allow_blank=True,
        required=False,
    )
    default_states = serializers.DictField(
        label=_('Default states'),
        help_text=_('Default workflow states'),
        source='defaultStates',
        default={}
    )


class FolderSerializer(serializers.Serializer):
    """
    Serializer for folder list
    """
    id = serializers.IntegerField(
        label=_('Folder numeric ID'),
        help_text=_('Folder internal numeric ID'),
        read_only=True,
        source='fcat_id'
    )
    uuid = serializers.UUIDField(
        label=_('Folder unique ID'),
        help_text=_('Folder unique ID'),
        read_only=True,
        source='folder_uuid'
    )
    parent_id = serializers.IntegerField(
        label=_('Folder parent ID'),
        help_text=_('Folder parent numeric ID'),
        read_only=True,
        source='fcat_parent_id'
    )
    name = serializers.CharField(
        label=_('Folder name'),
        help_text=_('Name of folder'),
        read_only=True,
        source='originalName'
    )
    decorated_name = serializers.CharField(
        label=_('Decorated name'),
        help_text=_('Name with decorations'),
        read_only=True,
        source='fcat_nom'
    )
    path = serializers.CharField(
        label=_('Folder path'),
        help_text=_('Folder full path'),
        read_only=True,
        source='fcat_chemin'
    )
    type = serializers.ChoiceField(
        label=_('Folder type'),
        help_text=_('0: normal folder, 2: folder excluded from search'),
        choices=[0, 2],
        default=0,
        read_only=True,
        source='fcat_type'
    )
    archived = serializers.BooleanField(
        label=_('Archived folder'),
        help_text=_('Folder has been archived'),
        default=False,
        read_only=True,
        source='fcat_flag'
    )
    created_at = serializers.DateTimeField(
        label=_('Folder created at'),
        help_text=_('Folder creation date'),
        format='%Y-%M-%D',
        read_only=True,
        source='fcat_createdate'
    )
    nb_files = serializers.IntegerField(
        label=_('Number of files'),
        help_text=_('Number of files contained in this folder'),
        read_only=True,
        source='nbInside'
    )
    nb_subfolders = serializers.IntegerField(
        label=_('Number of subfolders'),
        help_text=_('Number of subfolders contained in this folder'),
        read_only=True,
        source='nbsubfolders'
    )


class FolderDetailSerializer(FolderSerializer):
    """
    Serializer for folder retrieval
    """
    infos = serializers.SerializerMethodField(
        label=_('additional info'),
    )

    def get_infos(self, obj):
        if obj.get('fcat_desc'):
            try:
                json_desc = json.loads(obj.get('fcat_desc'))
                return FolderInfoSerializer(json_desc).data
            except json.JSONDecodeError:
                pass
        return None


class FolderCreateSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        label=_('Folder type'),
        help_text=_('0: normal folder, 2: folder excluded from search'),
        choices=[0, 2],
        default=0,
    )
    parent_id = serializers.IntegerField(
        label=_('Folder parent ID'),
        help_text=_('Folder parent numeric ID'),
        default=0,
        source='parentId'
    )
    name = serializers.CharField(
        label=_('Folder name'),
        help_text=_('Name of folder'),
        source='nom'
    )
    infos = FolderInfoSerializer(source='fcat_desc')



class FolderUpdateSerializer(serializers.Serializer):
    """
    Serializer to update folder name
    """
    name = serializers.CharField(
        label=_("Folder name"),
        help_text=_("Folder name"),
        required=True,
        source='nom'
    )
    infos = FolderInfoSerializer(source='fcat_desc')