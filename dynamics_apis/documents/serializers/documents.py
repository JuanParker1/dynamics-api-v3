"""
Serializers for documents
"""
from django.utils.translation import gettext as _
from rest_framework import serializers


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
    custom_fields = CustomFieldSerializer(many=True, source='customFields')
    custom_field_search = serializers.DictField(
        label=_('Search on custom fields'),
        help_text=_('Dictionnary in the form of {<rfield_uuid>:<value>}.'),
        source='searchByRField'
    )
    folder_id = serializers.IntegerField(
        label=_('ID of the folder'),
        help_text=_('numeric ID, use -1 to filter on archives, and -15989595 for personal folder'),
        source='id'
    )
    folder_ids = serializers.ListSerializer(
        label=_('List of parents'),
        help_text=_('List documents in multiple parent folders, exclusive with parent_id'),
        child=serializers.IntegerField(),
        source='multiid'
    )
    created_after = serializers.DateField(
        label=_('Document created after'),
        help_text=_('Exclusive date after which documents where created'),
        source='fromTimeAllDir'
    )
    created_before = serializers.DateField(
        label=_('Document created before'),
        help_text=_('Exclusive date before which documents where created'),
        source='endDate'
    )
    paper_copy = serializers.ChoiceField(
        label=_('Documents sent'),
        help_text=_(
            '0. Sent or not via paper copy, 1. Only sent via paper copy, 2, Only not sent via paper copy'),
        choices=[0, 1, 2],
        source='searchSendDateFlag'
    )
    sent_after = serializers.DateField(
        label=_('Document sent after'),
        help_text=_('Exclusive date after which documents was sent'),
        source='startSendDate'
    )
    sent_before = serializers.DateField(
        label=_('Document sent before'),
        help_text=_('Exclusive date before which documents where sent'),
        source='endSendDate'
    )
    updated_after = serializers.DateField(
        label=_('Documents updated after'),
        help_text=_('Exclusive date after which documents where updated'),
        source='files_update'
    )
    exclude_revision = serializers.UUIDField(
        label=_('Revision UUID to exclude'),
        help_text=_("Remove exclude revision from list"),
        source='exceludedUUIDRevision'
    )
    home_folder = serializers.IntegerField(
        label=_('Home folder'),
        help_text=_('Set -1 * user ID to filter on his home folder'),
        source='repPerso'
    )
    rfa = serializers.BooleanField(
        label=_('Documents with RFA'),
        help_text=_('Documents that require approval'),
        source='filesToVisas',
        default=False
    )
    approved = serializers.BooleanField(
        label=_('Documents with approval'),
        help_text=_('Documents that fave been approved'),
        source='filesVised'
    )
    workflows_union = serializers.ListSerializer(
        label=_('Submitted to one of the workflows'),
        help_text=_('List of dicts with workflow numeric ID and approvals'),
        child=serializers.DictField(),
        source='typedCircuit'
    )
    workflows_intersection = serializers.ListSerializer(
        label=_('Submitted to all workflows'),
        help_text=_('List of dicts with workflow numeric ID and approvals'),
        child=serializers.DictField(),
        source='typedCircuitAnd'
    )
    workflows_intersection_answered = serializers.ListSerializer(
        label=_('Submitted to all workflows and answered'),
        help_text=_('List of dicts with workflow numeric ID and approvals'),
        child=serializers.DictField(),
        source='typedCircuitAndWithAnswer'
    )
    workflows_intersection_unanswered = serializers.ListSerializer(
        label=_('Submitted to all workflows and unanswered'),
        help_text=_('List of dicts with workflow numeric ID and approvals'),
        child=serializers.DictField(),
        source='typedCircuitAndWithoutAnswer'
    )
    filter_on_parent_with_visa = serializers.ChoiceField(
        label=_('Filter operator'),
        help_text=_('Type of operator to apply to filter AND or OR'),
        choices=['AND', 'OR'],
        default='AND',
        source='filterTypeFilesLevelsVisaWith'
    )
    visa_without_answer_operator = serializers.ChoiceField(
        label=_('Filter operator'),
        help_text=_('Type of operator to apply to filter AND or OR'),
        choices=['AND', 'OR'],
        default='AND',
        source='filterTypeFilesLevelsVisaWithout'
    )



