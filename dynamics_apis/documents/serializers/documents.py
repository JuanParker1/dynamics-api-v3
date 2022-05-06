"""
Serializers for documents
"""
from django.utils.translation import gettext as _
from rest_framework import serializers

from dynamics_apis.common.serializers import CastingDateField


class CustomFieldSerializer(serializers.Serializer):
    id = serializers.UUIDField(
        label=_('UUID of the Rfield'),
        help_text=_('UUID of the Rfield'),
        source='guid'
    )
    value = serializers.CharField(
        label=_('value of the Rfield'),
        help_text=_('text value of the Rfield'),
    )


class DocumentQuerySerializer(serializers.Serializer):
    custom_fields = CustomFieldSerializer(
        many=True, source='customFields',
        required=False
    )
    custom_field_search = serializers.DictField(
        label=_('Search on custom fields'),
        help_text=_('Dictionnary in the form of {<rfield_uuid>:<value>}.'),
        source='searchByRField',
        allow_null=True,
        allow_empty=True,
        default={},
        required=False
    )
    uuid = serializers.UUIDField(
        label=_('Search documents by UUID'),
        help_text=_('Valid UUID'),
        source='search_by_uuid',
        required=False
    )
    folder_id = serializers.IntegerField(
        label=_('ID of the folder'),
        help_text=_('numeric ID, use -1 to filter on archives, and -15989595 for personal folder'),
        source='id',
        required=False
    )
    folder_ids = serializers.ListSerializer(
        label=_('List of parents'),
        help_text=_('List documents in multiple parent folders, exclusive with parent_id'),
        child=serializers.IntegerField(),
        source='multiid',
        required=False
    )
    folder_created_after = serializers.DateField(
        label=_('Document created after'),
        help_text=_('Exclusive date after which documents were created'),
        source='fromTimeAllDir',
        required=False
    )
    folder_created_before = serializers.DateField(
        label=_('Document created before'),
        help_text=_('Exclusive date before which documents were created'),
        source='endDate',
        required=False
    )
    paper_copy = serializers.ChoiceField(
        label=_('Documents sent'),
        help_text=_(
            '0. Sent or not via paper copy, 1. Only sent via paper copy, 2, Only not sent via paper copy'),
        choices=[0, 1, 2],
        source='searchSendDateFlag',
        required=False
    )
    sent_after = serializers.DateField(
        label=_('Document sent after'),
        help_text=_('Exclusive date after which documents was sent'),
        source='startSendDate',
        required=False
    )
    sent_before = serializers.DateField(
        label=_('Document sent before'),
        help_text=_('Exclusive date before which documents were sent'),
        source='endSendDate',
        required=False
    )
    files_updated_after = serializers.DateField(
        label=_('Documents updated after'),
        help_text=_('Exclusive date after which documents were updated'),
        source='files_update',
        required=False
    )
    exclude_revision = serializers.UUIDField(
        label=_('Revision UUID to exclude'),
        help_text=_("Remove exclude revision from list"),
        source='exceludedUUIDRevision',
        required=False
    )
    home_folder = serializers.IntegerField(
        label=_('Home folder'),
        help_text=_('Set -1 * user ID to filter on his home folder'),
        source='repPerso',
        required=False
    )
    rfa = serializers.BooleanField(
        label=_('Documents with RFA'),
        help_text=_('Documents that require approval'),
        source='filesToVisas',
        default=False,
        required=False
    )
    approved = serializers.BooleanField(
        label=_('Documents with approval'),
        help_text=_('Documents that have been approved'),
        source='filesVised',
        required=False
    )
    workflows_union = serializers.DictField(
        label=_('Submitted to one of the workflows'),
        help_text=_('Dictionary with workflow numeric ID and approvals'),
        source='typedCircuit',
        allow_null=True,
        allow_empty=True,
        default={},
        required=False
    )
    workflows_intersection = serializers.DictField(
        label=_('Submitted to all workflows'),
        help_text=_('Dictionary with workflow numeric ID and approvals'),
        source='typedCircuitAnd',
        allow_null=True,
        allow_empty=True,
        default={},
        required=False
    )
    workflows_intersection_answered = serializers.DictField(
        label=_('Submitted to all workflows and answered'),
        help_text=_('Dictionary with workflow numeric ID and approvals'),
        source='typedCircuitAndWithAnswer',
        allow_null=True,
        allow_empty=True,
        default={},
        required=False
    )
    workflows_intersection_unanswered = serializers.DictField(
        label=_('Submitted to all workflows and unanswered'),
        help_text=_('Dictionary with workflow numeric ID and approvals'),
        source='typedCircuitAndWithoutAnswer',
        allow_null=True,
        allow_empty=True,
        default={},
        required=False
    )
    operator_on_parent_with_visa = serializers.ChoiceField(
        label=_('Filter operator'),
        help_text=_('Type of operator to apply to filter AND or OR'),
        choices=['AND', 'OR'],
        default='AND',
        source='filterTypeFilesLevelsVisaWith',
        required=False
    )
    operator_visa_without_answer = serializers.ChoiceField(
        label=_('Filter operator'),
        help_text=_('Type of operator to apply to filter AND or OR'),
        choices=['AND', 'OR'],
        default='AND',
        source='filterTypeFilesLevelsVisaWithout',
        required=False
    )
    workflow_list = serializers.DictField(
        label=_('List of workflows and approvals'),
        help_text=_('Dictionary of workflow:[approvals]'),
        source='listeCircuits',
        allow_null=True,
        allow_empty=True,
        default={},
        required=False
    )
    late_approval = serializers.BooleanField(
        label=_('late approvals'),
        help_text=_('Display late approvals'),
        source='lateVisa',
        required=False
    )
    waiting_approval = serializers.BooleanField(
        label=_('In need of approval but not late'),
        help_text=_('In need of approval but not late'),
        source='needButNotLate',
        required=False
    )
    operator_must_be_stamped = serializers.ChoiceField(
        label=_('Filter operator'),
        help_text=_('Type of operator to apply to filter AND or OR'),
        choices=['AND', 'OR'],
        default='AND',
        source='filterTypeMustBeStamped',
        required=False
    )
    workflows_approved = serializers.DictField(
        label=_('Workflows that have been approved'),
        help_text=_('Dictionary with workflow numeric ID and approvals'),
        source='listeCircuitsVised',
        allow_null=True,
        allow_empty=True,
        default={},
        required=False
    )
    approved_by = serializers.IntegerField(
        label=_('User who approved a document'),
        help_text=_('User numeric ID'),
        source='userVisaSelected',
        required=False
    )
    operator_approved_by = serializers.ChoiceField(
        label=_('Filter operator'),
        help_text=_('Type of operator to apply to filter AND or OR'),
        choices=['AND', 'OR'],
        default='AND',
        source='filterTypeApprovedBy',
        required=False
    )
    approved_after = serializers.DateField(
        label=_('Approval given after'),
        help_text=_('Exclusive date after which approval was given'),
        source='startVisaDate',
        required=False
    )
    approved_before = serializers.DateField(
        label=_('Approval given before'),
        help_text=_('Exclusive date before which approval was given'),
        source='endVisaDate',
        required=False
    )
    archived = serializers.ChoiceField(
        label=_('Only retrieve archived files'),
        help_text=_(
            '0. Do not filter, 1. Archived documents in folder, 2. fetch archived documents from all folders'),
        choices=[0, 1, 2],
        source='only_archive',
        required=False
    )
    search = serializers.CharField(
        label=_('Search '),
        help_text=_('Simple document text search'),
        required=False
    )
    search_regex = serializers.CharField(
        label=_('Search with a regex'),
        help_text=_('Valid regular expression'),
        source='regex',
        required=False
    )
    search_naming_convention = serializers.DictField(
        label=_('Search elements of a naming convention'),
        help_text=_(
            'Dictionary with the convention ID as key and the value to search for as value'),
        source='searchListNomenclature',
        allow_null=True,
        allow_empty=True,
        default={},
        required=False
    )
    operator_search = serializers.ChoiceField(
        label=_('Filter operator'),
        help_text=_('Type of operator to apply to filter AND or OR'),
        choices=['AND', 'OR'],
        default='AND',
        source='searchType',
        required=False
    )
    last_version = serializers.BooleanField(
        label=_('Only retrieve latest version'),
        help_text=_('Only retrieve latest version'),
        source='onlyLastVersion',
        required=False
    )
    deposit = serializers.IntegerField(
        label=_('filter on deposit ID'),
        help_text=_('Deposit numeric ID'),
        source='statementWantedId',
        required=False
    )
    has_deposit = serializers.ChoiceField(
        label=_('Filter on documents with deposit'),
        help_text=_('0. all documents, 1. only with deposit, 2. only without deposit'),
        choices=[0, 1, 2],
        source='statementState',
        required=False
    )
    paper_deposit = serializers.IntegerField(
        label=_('filter on paper deposit ID'),
        help_text=_('Deposit numeric ID'),
        source='printStatementWantedId',
        required=False
    )
    has_paper_deposit = serializers.ChoiceField(
        label=_('Filter on documents with paper deposit'),
        help_text=_('0. all documents, 1. only with deposit, 2. only without deposit'),
        choices=[0, 1, 2],
        source='printStatementState',
        required=False
    )
    created_after = serializers.DateField(
        label=_('Approval given after'),
        help_text=_('Exclusive date after which document was modified'),
        source='creation_start',
        required=False
    )
    created_before = serializers.DateField(
        label=_('Approval given before'),
        help_text=_('Exclusive date before which document was modified'),
        source='creation_end',
        required=False
    )
    updated_after = serializers.DateField(
        label=_('Approval given after'),
        help_text=_('Exclusive date after which document was modified'),
        source='modification_start',
        required=False
    )
    updated_before = serializers.DateField(
        label=_('Approval given before'),
        help_text=_('Exclusive date before which document was modified'),
        source='modification_end',
        required=False
    )


class DocumentSerializer(serializers.Serializer):
    """
    Base Document serializer
    """
    group_id = serializers.UUIDField(
        label=_('Group ID'),
        help_text=_('UUID of the parent group'),
        source='groupe_uuid',
        read_only=True,
        required=False
    )
    id = serializers.IntegerField(
        label=_('Document numeric ID'),
        help_text=_('Numeric ID of the document'),
        source='item_id',
        read_only=True,
        required=False
    )
    uuid = serializers.UUIDField(
        label=_('Document unique ID'),
        help_text=_('Unique ID of the document'),
        read_only=True,
        required=False
    )
    folder_id = serializers.IntegerField(
        label=_('Folder numeric ID'),
        help_text=_('Numeric ID of the folder'),
        source='cat_id',
        read_only=True,
        required=False
    )
    name = serializers.CharField(
        label=_('Document name'),
        help_text=_('Name of the document in a naming convention'),
        read_only=True,
        source='entete_nom',
        required=False
    )
    extension = serializers.CharField(
        label=_('File extension'),
        help_text=_('Extension of the original file'),
        read_only=True,
        source='entete_ext',
        required=False
    )
    original_name = serializers.CharField(
        label=_('Document upload name'),
        help_text=_('Name of the document as uploaded'),
        read_only=True,
        source='entete_oldName',
        required=False
    )
    type = serializers.CharField(
        label=_('File type'),
        help_text=_('Type of the uploaded file'),
        read_only=True,
        source='entete_type',
        required=False
    )
    description = serializers.CharField(
        label=_('Document description'),
        help_text=_('Description of the document'),
        read_only=True,
        source='entete_desc',
        required=False
    )
    file_date = serializers.CharField(
        label=_('Date of file'),
        help_text=_('Date of the upload'),
        read_only=True,
        source='entete_date',
        required=False
    )
    file_size = serializers.IntegerField(
        label=_('File size'),
        help_text=_('Size of the uploaded file'),
        read_only=True,
        source='entete_size',
        required=False
    )
    file_preview = serializers.CharField(
        label=_('File preview'),
        help_text=_('Preview of the uploaded file'),
        read_only=True,
        source='entete_image',
        required=False
    )
    workflow = serializers.CharField(
        label=_('Workflow'),
        help_text=_('Workflow of the document'),
        read_only=True,
        source='circuit',
        required=False
    )
    file_update = serializers.DateField(
        label=_('File updated at'),
        help_text=_('Date of update of the file, not the document'),
        read_only=True,
        source='files_update',
        required=False
    )
    created_by_id = serializers.IntegerField(
        label=_('creator numeric ID'),
        help_text=_('Numeric ID of the creator'),
        read_only=True,
        source='entete_createby',
        required=False
    )
    created_by_full_name = serializers.CharField(
        label=_('creator full name'),
        help_text=_('First name and last name of the creator'),
        read_only=True,
        source='createby',
        required=False
    )
    created_by_email = serializers.CharField(
        label=_('creator email'),
        help_text=_('e-mail of the creator'),
        read_only=True,
        source='user_email',
        required=False
    )
    tags = serializers.CharField(
        label=_('Document tags'),
        help_text=_('Aggregated tags applied to document'),
        read_only=True,
        required=False
    )
    system_tags = serializers.ListSerializer(
        label=_('Document system tags'),
        help_text=_('Aggregated system tags applied to document'),
        child=serializers.CharField(),
        read_only=True,
        source='tags',
        required=False
    )
    archived = serializers.BooleanField(
        label=_('Archived document'),
        help_text=_('Document has been archived'),
        read_only=True,
        source='entete_archive',
        required=False
    )
    nb_of_revisions = serializers.IntegerField(
        label=_('Number of revisions'),
        help_text=_('Revisions for a document'),
        read_only=True,
        source='files_nbrev',
        required=False
    )
    full_path = serializers.CharField(
        label=_('Document path'),
        help_text=_('Full path of the document'),
        read_only=True,
        source='files_path',
        required=False
    )
    last_revision = serializers.CharField(
        label=_('Last revision'),
        help_text=_('Last revision number of the document'),
        read_only=True,
        source='files_lastRev',
        required=False
    )
    converted_file = serializers.BooleanField(
        label=_('Converted file'),
        help_text=_('Uploaded file has been converted'),
        read_only=True,
        source='files_converted',
        required=False
    )
    infos = serializers.CharField(
        label=_('Additional information'),
        help_text=_('File additional JSON information'),
        read_only=True,
        source='files_infos',
        required=False
    )
    checksum = serializers.CharField(
        label=_('Checksum'),
        help_text=_('Uploaded file checksum'),
        read_only=True,
        source='files_crc',
        required=False
    )
    file_id = serializers.IntegerField(
        label=_('File ID'),
        help_text=_('ID of the uploaded file'),
        read_only=True,
        source='files_id',
        required=False
    )
    parent_id = serializers.IntegerField(
        label=_('Parent document ID'),
        help_text=_('Numeric ID of the parent document'),
        read_only=True,
        source='entete_parentid',
        required=False
    )
    parent_uuid = serializers.UUIDField(
        label=_('Parent document unique ID'),
        help_text=_('Unique ID of the parent document'),
        read_only=True,
        required=False
    )
    version = serializers.IntegerField(
        label=_('Document version'),
        help_text=_('Numeric ID of the parent document'),
        read_only=True,
        source='entete_version',
        required=False
    )
    deposit_info = serializers.CharField(
        label=_('Deposit info'),
        help_text=_('serialized JSON info on the deposit'),
        read_only=True,
        source='statements',
        required=False
    )
    paper_deposit_info = serializers.CharField(
        label=_('Paper deposit info'),
        help_text=_('serialized JSON info on the paper deposit'),
        read_only=True,
        source='printStatements',
        required=False
    )
    sent_date = serializers.DateField(
        label=_('Document send date'),
        help_text=_('Date of the document deposit'),
        read_only=True,
        source='files_sendDate',
        required=False
    )
    naming_convention = serializers.CharField(
        label=_('Naming convention'),
        help_text=_('Convention ID applied to the document'),
        read_only=True,
        source='entete_nomenclature',
        required=False
    )
    approved_by = serializers.IntegerField(
        label=_('Validator ID'),
        help_text=_('Numeric ID of the validator'),
        read_only=True,
        source='files_validation_by',
        required=False
    )
    approved_by_full_name = serializers.CharField(
        label=_('validator full name'),
        help_text=_('First name and last name of the validator'),
        read_only=True,
        source='validationby',
        required=False
    )
    approved_date = serializers.DateField(
        label=_('Document approval date'),
        help_text=_('Date of the document approval'),
        read_only=True,
        source='files_validation_date',
        required=False
    )
    folder_path = serializers.CharField(
        label=_('Folder path'),
        help_text=_('Path of the folder'),
        read_only=True,
        source='fcat_chemin',
        required=False
    )
    stamp_info = serializers.CharField(
        label=_('Stamp path'),
        help_text=_('Path of the stamped file'),
        read_only=True,
        source='files_pathSecondary',
        required=False
    )
    forecast_info = serializers.JSONField(
        label=_('Forecast information'),
        help_text=_('Forecast JSON data'),
        read_only=True,
        source='previsionalData',
        required=False
    )
    contacts = serializers.CharField(
        label=_('Contacts'),
        help_text=_('Concatenated list of contact IDs'),
        read_only=True,
        source='linkedContacts',
        required=False
    )
    all_extensions = serializers.CharField(
        label=_('Extensions'),
        help_text=_('Concatenated list of extensions'),
        read_only=True,
        source='fileExtensionList',
        required=False
    )


class LinkedObjectSerializer(serializers.Serializer):
    """
    Serializer for linked objects
    """
    uuid = serializers.UUIDField(
        label=_('Linked Object UUID'),
        help_text=_('UUID of the object linked to the document'),
        required=True
    )
    type = serializers.CharField(
        label=_('type of object'),
        help_text=_('Type of the object linked to the document'),
        required=True
    )
    dest_type = serializers.CharField(
        label=_('destination type'),
        help_text=_('Type of the destination object'),  # TODO: What is that ?
        required=False
    )


class DocumentFilterSerializer(serializers.Serializer):
    """
    Serializer to handle document query filter from $_FILES_FILTERS
    """
    approved_documents = serializers.ChoiceField(
        label=_('Approved documents'),
        help_text=_('ALL to see al approved documents'),
        choices=['ALL', ''],
        required=False,
        allow_blank=True,
        allow_null=True,
        source='filesVised'
    )
    approved_workflows = serializers.JSONField(
        label=_('documents with workflow approved'),
        help_text=_('{"dictionnary of workflows and steps: workflow_id": [steps], }'),
        allow_null=True,
        required=False,
        source='listeCircuitsVised',
        default={}
    )
    documents_to_approve = serializers.BooleanField(
        label=_('filter on documents to approve'),
        help_text=_('Boolean value'),
        allow_null=True,
        required=False,
        default=False,
        source='filesToVisas'
    )
    print_statement = serializers.IntegerField(
        label=_('Document statement'),
        help_text=_('0: all statements, 1: with statement, 2: without statement'),
        default=0,
        source='printStatementState'

    )
    statement = serializers.IntegerField(
        label=_('Document statement'),
        help_text=_('0: all statements, 1: with statement, 2: without statement'),
        default=0,
        source='statementState'
    )
    global_check = serializers.BooleanField(
        label=_('Get all files'),
        help_text=_('if true, list all files, whether or not they are in the folder'),
        source='overallCheck',
        default=False
    )
    created_by = serializers.ListSerializer(
        label=_('createor IDs'),
        help_text=_('List of creator ids'),
        required=True,
        child=serializers.IntegerField(),
        source='createByUsers'
    )
    custom_fields = CustomFieldSerializer(
        label=_('Custom fields'),
        help_text=_('List of custom fields'),
        many=True,
        required=False,
        allow_null=True,
        source='customFields'
    )
    uuid = serializers.UUIDField(
        label=_('Document UUID'),
        help_text=_('UUID of the document in the string form'),
        allow_null=True,
        required=False,
        source='search_by_uuid'
    )
    id = serializers.IntegerField(
        label=_('Document numeric ID'),
        help_text=_('Numeric ID of the document'),
        allow_null=True,
        required=False,
        source='getSingleID'
    )
    workflow_list = serializers.JSONField(
        label=_('documents with workflow'),
        help_text=_('{"dictionnary of workflows and steps: workflow_id": [steps], }'),
        allow_null=True,
        required=False,
        source='listCircuits',
        default={}
    )
    created_after = serializers.DateField(
        label=_('Documents created after date'),
        help_text=_('Document with createdate > date'),
        allow_null=True,
        required=False,
        source='fromTimeAllDir'
    )
    created_before = serializers.DateField(
        label=_('Documents created before date'),
        help_text=_('Document with approval date before date'),
        allow_null=True,
        required=False,
        source='endDate'
    )
    to_approval_date = serializers.DateField(
        label=_('Approval date below'),
        help_text=_('Document with approval date lower than date'),
        allow_null=True,
        required=False,
        source='endVisaDate'
    )
    from_approval_date = serializers.DateField(
        label=_('Approval date after'),
        help_text=_('Document with approval date after date'),
        allow_null=True,
        required=False,
        source='startVisaDate'
    )
    sent = serializers.ChoiceField(
        label=_('Sent documents'),
        help_text=_('0: all values, 1: with paper sent date, 2: without paper sent date'),
        choices=[0, 1, 2],
        default=0,
        source='searchSendDateFlag'
    )
    to_send_date = serializers.DateField(
        label=_('Send date below'),
        help_text=_('Document with send date lower than date'),
        allow_null=True,
        required=False,
        source='endSendDate'
    )
    from_send_date = serializers.DateField(
        label=_('Send date after'),
        help_text=_('Document with send date after date'),
        allow_null=True,
        required=False,
        source='startSendDate'
    )
    answered_approvals = serializers.JSONField(
        label=_('documents with answered approvals'),
        help_text=_('{"dictionnary of workflows and steps: workflow_id": [steps], }'),
        allow_null=True,
        required=False,
        source='typedCircuitAndWithAnswer',
        default={}
    )
    unanswered_approvals = serializers.JSONField(
        label=_('documents without answered approvals'),
        help_text=_('{"dictionnary of workflows and steps: workflow_id": [steps], }'),
        allow_null=True,
        required=False,
        source='typedCircuitAndWithoutAnswer',
        default={}
    )
    approvers = serializers.ListSerializer(
        label=_('List of approvers'),
        help_text=_('List of user IDs'),
        source='userVisaSelected',
        child=serializers.IntegerField(),
        required=False
    )
    search = serializers.CharField(
        label=_('Regex search of file'),
        help_text=_('Search with a regular expression'),
        source='regex',
        allow_null=True
    )


class RFieldSerializer(serializers.Serializer):
    """
    Serializer for rField attached to a document
    """
    uuid = serializers.UUIDField(
        label=_('rField UUID'),
        help_text=_('UUID of the metadata'),
        required=True
    )
    value = serializers.CharField(
        label=_('rField value'),
        help_text=_('Value of the metadata'),
        required=True
    )
    type = serializers.CharField(
        label=_('rField type'),
        help_text=_('Type of the metadata'),
        required=True
    )


class DocumentSearchPathSerializer(serializers.Serializer):
    """
    Serializer for document path
    """
    folder_path = serializers.CharField(
        label=_('Folder path'),
        help_text=_('Folder path, can be created if not exists using create_folders parameter'),
        required=False,
        source='path'
    )


class DocumentSearchRevisionSerializer(serializers.Serializer):
    """
    Serializer to search for existing document when
    """
    name = serializers.CharField(
        label=_('Document name'),
        help_text=_('Name of the document'),
        source='entete_nom',
        required=True,
    )
    naming_convention = serializers.IntegerField(
        label=_('Naming convention ID'),
        help_text=_('Numeric ID of the naming convention'),
        required=False,
        default=0,
        source='entete_nomenclature'
    )
    parent = serializers.UUIDField(
        label=_('Main document ID'),
        help_text=_('UUID of the parent document'),
        required=False,
        source='parent_uuid'
    )
    id = serializers.IntegerField(
        label=_('Document numeric ID'),
        help_text=_('Numeric ID of the document'),
        source='item_id',
        default=0
    )


class DocumentExtensionSerializer(serializers.Serializer):
    extension = serializers.CharField(source='ext')
    path = serializers.CharField()
    file_id = serializers.IntegerField()


class DocumentRevisionSerializer(serializers.Serializer):
    """
    Serialize result of GetFileRevision
    """
    group_id = serializers.UUIDField(
        label=_('Group ID'),
        help_text=_('UUID of the parent group'),
        source='groupe_uuid',
        read_only=True,
        required=False
    )
    id = serializers.IntegerField(
        label=_('Document ID'),
        help_text=_('Document numeric ID'),
        read_only=True,
        source='item_id'
    )
    folder_id = serializers.IntegerField(
        label=_('Folder ID'),
        help_text=_('Folder numeric ID'),
        read_only=True,
        source='cat_id'
    )
    name = serializers.CharField(
        label=_('Document name'),
        help_text=_('Name of the document'),
        read_only=True,
        source='entete_nom'
    )
    extension = serializers.CharField(
        label=_('File extension'),
        help_text=_('Extension of the file'),
        read_only=True,
        source='entete_ext'
    )
    link_extension = serializers.CharField(
        label=_('File extension for link'),
        help_text=_('Extension of the file used in link'),
        read_only=True,
        source='entete_extForLink'
    )
    external_name = serializers.CharField(
        label=_('Document name as uploaded'),
        help_text=_('Name of the document when uploaded'),
        source='entete_oldName',
        read_only=True
    )
    type = serializers.CharField(
        label=_('File type'),
        help_text=_('MIME type of the file'),
        source='files_type',
        read_only=True
    )
    description = serializers.CharField(
        label=_('Document description'),
        help_text=_('Description of the document'),
        read_only=True,
        source='files_desc'
    )
    file_date = CastingDateField(
        label=_('Date of file'),
        help_text=_('Date of the upload'),
        read_only=True,
        source='files_date'
    )
    file_size = serializers.IntegerField(
        label=_('File size'),
        help_text=_('Size of the uploaded file'),
        read_only=True,
        source='files_size'
    )
    workflow = serializers.CharField(
        label=_('Workflow'),
        help_text=_('Workflow of the document'),
        read_only=True,
        source='circuit'
    )
    created_by_id = serializers.IntegerField(
        label=_('creator numeric ID'),
        help_text=_('Numeric ID of the creator'),
        read_only=True,
        source='entete_createby'
    )
    created_by_link_id = serializers.IntegerField(
        label=_('creator numeric ID'),
        help_text=_('Numeric ID of the creator'),
        read_only=True,
        source='entete_createbyForLink'
    )
    archive = serializers.BooleanField(
        label=_('Archived document'),
        help_text=_('Document has been archived'),
        read_only=True,
        source='entete_archive'
    )
    revision_count = serializers.IntegerField(
        label=_('Nb of revisions'),
        help_text=_('Number of revisions, 1 means there is only one version'),
        read_only=True,
        source='files_nbrev'
    )
    last_revision = serializers.CharField(
        label=_('Last revision number'),
        help_text=_('Number of the last revision'),
        read_only=True,
        source=_('files_lastRev')
    )
    version = serializers.IntegerField(
        label=_('Version number'),
        help_text=_('Automatic or manual version number'),
        read_only=True,
        source='entete_version'
    )
    converted = serializers.BooleanField(
        label=_('Converted file'),
        help_text=_('File has been converted'),
        read_only=True,
        source='files_converted'
    )
    file_id = serializers.IntegerField(
        label=_('File ID'),
        help_text=_('Numeric ID of the file'),
        read_only=True,
        source='files_id'
    )
    parent_id = serializers.IntegerField(
        label=_('Parent ID'),
        help_text=_('Numeric ID of the parent file'),
        read_only=True,
        source='entete_parentId'
    )
    created_at = serializers.CharField(
        label=_('Date of document'),
        help_text=_('Date of the document creation'),
        read_only=True,
        source='entete_createdate',
        required=False
    )
    tags = serializers.ListSerializer(
        label=_('Document tags'),
        help_text=_('Aggregated tags applied to document'),
        child=serializers.CharField(),
        read_only=True,
        required=False
    )
    system_tags = serializers.CharField(
        label=_('Document system tags'),
        help_text=_('Aggregated system tags applied to document'),
        read_only=True,
        required=False
    )
    naming_convention = serializers.IntegerField(
        label=_('Naming convention ID'),
        help_text=_('Numeric ID of the naming convention'),
        required=False,
        default=0,
        source='entete_nomenclature'
    )
    approved_by = serializers.IntegerField(
        label=_('Validator ID'),
        help_text=_('Numeric ID of the validator'),
        read_only=True,
        source='files_validation_by',
        required=False
    )
    approved_date = serializers.DateField(
        label=_('Document approval date'),
        help_text=_('Date of the document approval'),
        read_only=True,
        source='files_validation_date',
        required=False
    )
    folder_path = serializers.CharField(
        label=_('Folder path'),
        help_text=_('Path of the folder'),
        read_only=True,
        source='fcat_chemin',
        required=False
    )
    sent_date = serializers.DateField(
        label=_('Document send date'),
        help_text=_('Date of the document deposit'),
        read_only=True,
        source='files_sendDate',
        required=False
    )
    stamp_info = serializers.CharField(
        label=_('Stamp path'),
        help_text=_('Path of the stamped file'),
        read_only=True,
        source='files_pathSecondary',
        required=False
    )
    forecast_info = serializers.JSONField(
        label=_('Forecast information'),
        help_text=_('Forecast JSON data'),
        read_only=True,
        source='previsionalData',
        required=False
    )
    contacts = serializers.CharField(
        label=_('Contacts'),
        help_text=_('Concatenated list of contact IDs'),
        read_only=True,
        source='linkedContacts',
        required=False
    )
    all_extensions = DocumentExtensionSerializer(
        many=True,
        source='fileExtensionList',
        read_only=True
    )


class DocumentRevisionTreeSerializer(DocumentRevisionSerializer):
    revisions = DocumentRevisionSerializer(
        label=_('document revisions'),
        help_text=_('List of document revisions'),
        read_only=True,
        many=True
    )


class DocumentSearchRevisionSupplementaryArguments(serializers.Serializer):
    """
    Serializer for revision search additional arguments (folder id)
    """
    folder_id = serializers.IntegerField(
        label=_('Folder ID'),
        help_text=_('Restrict search on folder ID'),
        source='folderRestricionId',
        read_only=True,
        required=False
    )
    is_sending = serializers.BooleanField(
        label=_('Is sending'),
        help_text=_('Check all files before sending'),
        source='isSending',
        default=True
    )


class DocumentCreateSerializer(serializers.Serializer):
    """
    Serializer for document creation
    """
    category = serializers.IntegerField(
        label=_('Category'),
        help_text=_('Optional numeric ID of the category'),
        required=False,
        default=0
    )
    name = serializers.CharField(
        label=_('Document name'),
        help_text=_('Name of the document'),
        source='nom',
        required=False
    )
    file = serializers.FileField(
        label=_('File to upload'),
        help_text=_('File'),
        required=True
    )
    description = serializers.CharField(
        label=_('Document description'),
        help_text=_('Description of the document'),
        source='desc',
        required=False
    )
    external_name = serializers.CharField(
        label=_('Document name as uploaded'),
        help_text=_('Name of the document when uploaded'),
        source='entete_oldName',
        required=False
    )
    counter = serializers.IntegerField(
        label=_('Document counter'),
        help_text=_('Counter value of the document'),
        required=False,
        default=0
    )
    advanced = serializers.BooleanField(
        label=_('Advanced naming'),
        help_text=_('Automatic document naming'),
        required=False
    )
    naming_convention = serializers.IntegerField(
        label=_('Naming convention ID'),
        help_text=_('Numeric ID of the naming convention'),
        required=False,
        default=0,
        source='nomenclatureID'
    )
    parent = serializers.UUIDField(
        label=_('Parent ID'),
        help_text=_('UUID of the parent document'),
        required=False,
        source='parentUUID'
    )
    version = serializers.IntegerField(
        label=_('Document version'),
        help_text=_('Numeric version of the document'),
        required=False,
        default=0,
        source='enteteVersion'
    )
    workflow = serializers.IntegerField(
        label=_('Document workflow'),
        help_text=_('Numeric ID of the document workflow'),
        required=False,
        source='circuit'
    )
    linked_objects = LinkedObjectSerializer(
        label=_('List of objects to link'),
        help_text=_('List of objects from the platform to link to the document'),
        many=True,
        required=False
    )
    previous_uuid = serializers.UUIDField(
        label=_('Previous UUID'),
        help_text=_('UUID of the existing document'),
        required=False,
        source='oldUuid'
    )
    rfas = serializers.JSONField(
        label=_('List of RFAs'),
        help_text=_('Requests for approval for this document'),
        required=False,
        source='visas'
    )
    rfields = RFieldSerializer(
        label=_('List off rfields'),
        help_text=_('Meta data associated with the document'),
        many=True,
        required=False,
        source='rfield'
    )
    provisional_file = serializers.UUIDField(
        label=_('Provisional file UUID'),
        help_text=_('UUID of the attached provisional file '),
        required=False,
        source='attachedProvisionalFile'
    )
    skip_qr_code = serializers.BooleanField(
        label=_('Skip QRcode creation'),
        help_text=_('Do not create a QRCode for this file'),
        default=False
    )
    folder_path = serializers.CharField(
        label=_('Folder path'),
        help_text=_('Folder path, can be created if not exists using create_folders parameter'),
        required=False,
        source='path'
    )
    create_folders = serializers.BooleanField(
        label=_('Create folder if not exists'),
        help_text=_('Create folder from folder_path if the folder path does not exist'),
        default=True,
        source='createFolders'
    )


class FileUploadSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(
        label=_('file UUID'),
        help_text=_('UUID of the file'),
    )
    files_path = serializers.CharField(
        label=_('File path'),
        help_text=_('Technical path of the file')
    )
    method = serializers.CharField(
        label=_('Upload method'),
        help_text=_('HTTP method for the upload')
    )
    url = serializers.URLField(
        label=_('File upload URL'),
        help_text=_('URL to uplaod the content to')
    )


class DocumentReviseSerializer(DocumentCreateSerializer):
    pass
