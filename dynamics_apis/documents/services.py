"""
Services that get and push information to Kairnial WS servers
"""
import json
from django.conf import settings
from dynamics_apis.common.services import KairnialWSService


class FolderService(KairnialWSService):
    """
    Service that fetches and pushes folders
    """
    service_domain = 'fichiers'

    def list(self, parent_id: str = None, filters: dict = None):
        """
        List folders
        :param parent_id: ID of the parent folder, optional
        :return:
        """
        parameters = []
        if filters:
            parameters = [{key: value} for key, value in filters.items()]
        if parent_id:
            parameters.append({'asyncFolderId': parent_id})
        print(parameters)
        return self.call(action='getFlexDossiers', parameters=parameters)

    def get(self, id: int):
        """
        List folders
        :param parent_id: ID of the parent folder, optional
        :return:
        """
        return self.call(action='getFlexDossiers', parameters=[{'getById': id}])

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
            parameters=[folder_create_serializer],
            use_cache=False
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
            format='int',
            use_cache=False
        )

    def archive(self, id: str):
        """
        Archive a Kairnial folder
        :param id: UUID of the folder
        """
        return self.call(
            action='archiveIt',
            parameters=[{'uuid': id}, ],
            format='int',
            use_cache=False
        )


class DocumentService(KairnialWSService):
    """
    Service that fetches and push documents
    """
    service_domain = 'fichiers'

    def list(self, parent_id: str = None, filters: dict = None, offset: int = 0, limit: int = getattr(settings, 'PAGE_SIZE', 100)):
        """
        List documents
        :param parent_id: ID of the parent folder, optional
        :param filters: Dictionnary of filters
        :param offset: value of first element in a list
        :param limit: number of elements to fetch
        :return:
        """
        parameters = []
        if filters:
            parameters = [{key: value} for key, value in filters.items()]
        if parent_id:
            parameters.append({'asyncFolderId': parent_id})
        parameters += [
            {'LIMITSKIP': offset},
            {'LIMITTAKE': limit}
        ]
        print(parameters)
        return self.call(action='getFilesFromCat', parameters=parameters)