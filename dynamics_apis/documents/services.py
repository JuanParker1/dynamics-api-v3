"""
Services that get and push information to Kairnial WS servers
"""
import json
import logging
import time
import uuid

import requests
from django.conf import settings

from dynamics_apis.common.services import KairnialWSService, KairnialWSServiceError
from .serializers.documents import FileUploadSerializer

REQUESTS_METHODS = {
    'put': requests.put,
    'post': requests.post,
    'get': requests.get
}


class KairnialFolderService(KairnialWSService):
    """
    Service that fetches and pushes folders
    """
    service_domain = 'fichiers'

    def list(self, parent_id: str = None, filters: dict = None):
        """
        List folders
        :param parent_id: ID of the parent folder, optional
        :param filters: key: value filters
        :return:
        """
        parameters_dict = {}
        if filters:
            parameters_dict = {key: value for key, value in filters.items() if value}
        if parent_id:
            parameters_dict['asyncFolderId'] = parent_id
        return self.call(action='getFlexDossiers', parameters=[parameters_dict])

    def get(self, id: int):
        """
        List folders
        :param id: ID of the parent folder, optional
        :return:
        """
        return self.call(action='getFlexDossiers', parameters=[{'getById': id}], use_cache=True)

    def create(self, folder_create_serializer: {}):
        """
        Create a Kairnial folder
        :param folder_create_serializer: validated data from a FolderCreateSerializer
        """
        try:
            folder_create_serializer['fcat_desc'] = json.dumps(
                folder_create_serializer['fcat_desc'])
        except json.JSONDecodeError:
            return False
        return self.call(
            action='addDossier',
            parameters=[folder_create_serializer]
        )

    def update(self, id: int, folder_update_serializer: {}):
        """
        Update a Kairnial Folder
        :param folder_update_serializer: validated data from a FolderUpdateSerializer
        :param id: Numeric of the contact
        """
        folder_update_serializer['id'] = id
        try:
            folder_update_serializer['fcat_desc'] = json.dumps(
                folder_update_serializer['fcat_desc'])
        except json.JSONDecodeError:
            return False
        return self.call(
            action='updateDossier',
            parameters=[folder_update_serializer, ],
            out_format='int'
        )

    def archive(self, id: str):
        """
        Archive a Kairnial folder
        :param id: UUID of the folder
        """
        return self.call(
            action='archiveIt',
            parameters=[{'uuid': id}, ],
            out_format='int'
        )


class KairnialDocumentService(KairnialWSService):
    """
    Service that fetches and push documents
    """
    service_domain = 'fichiers'

    def list(self, parent_id: str = None, filters: dict = None, offset: int = 0,
             limit: int = getattr(settings, 'PAGE_SIZE', 100)):
        """
        List documents
        :param parent_id: ID of the parent folder, optional
        :param filters: Dictionnary of filters
        :param offset: value of first element in a list
        :param limit: number of elements to fetch
        :return:
        """
        parameters_dict = {
            'LIMITSKIP': offset,
            'LIMITTAKE': limit
        }
        if parent_id:
            parameters_dict['fcat_id'] = parent_id
        if filters:
            parameters_dict.update({key: value for key, value in filters.items() if value})
        return self.call(action='getFilesFromCat', parameters=[parameters_dict])

    def _get_file_link(self, json_data):
        """
        Get a file link for upload
        """
        logger = logging.getLogger('services')
        file_uuid = str(uuid.uuid4())
        prepare_file_parameters = {
            'name': json_data.get('nom'),
            'ext': json_data.get('ext'),
            'size': json_data.get('size'),
            'lastModified': int(time.time()),
            'type': json_data.get('typeFichier'),
            'guid': file_uuid
        }
        # 1. Obtain the upload link
        response = self.call(
            action='prepareFileUpload',
            parameters=[prepare_file_parameters]
        )
        us = FileUploadSerializer(data=response)
        if not us.is_valid():
            logger.error(us.errors)
            raise KairnialWSServiceError(
                message='Invalid response from file upload',
                status=0
            )
        return us

    def _create_document(self, file_uuid, json_data):
        data = json_data.copy()
        data['uuid'] = file_uuid
        try:
            data['rfield'] = json.dumps(
                json_data.get('rfield', []))
            data['linkedObjects'] = json.dumps(
                json_data.get('linkedObjects', []))
            data['visas'] = json.dumps(
                json_data.get('visas', []))
            data.pop('file')
        except json.JSONDecodeError:
            return False

        output = self.call(
            action='addFile',
            parameters=[data, ]
        )
        if 'error' in output:
            raise KairnialWSServiceError(
                message=output.get('error'),
                status=output.get('errorCode')
            )
        return output

    def get(self, id: int):
        """
        Retrieve document
        :param id: ID of the document
        :return:
        """
        return self.call(action='getFilesFromCat', parameters=[{'getSingleID': id}], use_cache=True)

    def create(self, document_create_serializer: dict, content):
        """
        Create a Kairnial folder
        :param document_create_serializer: validated data from a DocumentCreateSerializer
        :param content: Binary file content
        """
        # 1. GET file link
        us = self._get_file_link(json_data=document_create_serializer)

        # 2. POST file to url
        REQUESTS_METHODS[us.validated_data.get('method').lower()](
            us.validated_data.get('url'),
            data=content,
        )

        # 3. Create Document with file
        output = self._create_document(
            file_uuid=us.validated_data.get('uuid'),
            json_data=document_create_serializer
        )
        return output

    def revise(self, document_revise_serializer: dict, content):
        """
        Create a Kairnial folder
        :param document_revise_serializer: validated data from a DocumentReviseSerializer
        :param content: Binary file content
        """
        # 1. Get file link
        us = self._get_file_link(json_data=document_revise_serializer)

        # 2. POST file to url
        REQUESTS_METHODS[us.validated_data.get('method').lower()](
            us.validated_data.get('url'),
            data=content
        )

        # 3. Create Document with file
        output = self._create_document(
            file_uuid=us.validated_data.get('uuid'),
            json_data=document_revise_serializer
        )

        return output

    def archive(self, id: int):
        """
        Archive a Kairnial document
        :param id: Numeric ID of the document
        """
        return self.call(
            action='archiveFile',
            parameters=[{'id': id}, ],
            out_format='int'
        )

    def check_revision(
            self,
            document_search_revision_serializer: dict,
            supplementary_info_serializer: dict,
            check_extension: bool):
        """
        Check if a document exists
        """
        parameters = [
            [document_search_revision_serializer, ],
            supplementary_info_serializer,
            check_extension]
        return self.call(action='getFilesForRevision', parameters=parameters)


class KairnialApprovalTypeService(KairnialWSService):
    """
    Kairnial Service for Document Approval types
    """
    service_domain = 'fichiers'

    def list(self):
        """
        List approval types
        :return:
        """
        return self.call(action='getAllCircuitVisa', use_cache=True)

    def archive(self, id: int):
        """
        Archive approval type
        :param id: Numeric ID of the approval type
        """
        return self.call(
            action='archiveCircuitVisa',
            parameters=[{'id': id}, ],
            out_format='int'
        )


class KairnialApprovalService(KairnialWSService):
    """
    Kairnial service for approvals
    """
    service_domain = 'fichiers'

    def list(self):
        """
        List approvals for a set of documents
        """
        return self.call(
            action='getFilesHeaderAndVisas',
            use_cache=True
        )

    def update(self, document_id, workflow_id, approval_id, new_status):
        """
        Archive existing pproval step and create a new one
        """
        parameters = [document_id, workflow_id, approval_id, new_status]
        return self.call(
            action='updateVisaNeeded',
            parameters=parameters
        )
