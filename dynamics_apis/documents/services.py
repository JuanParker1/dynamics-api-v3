"""
Services that get and push information to Kairnial WS servers
"""
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
            parameters['asyncFolderId'] = parent_id
        return self.call(action='getFlexDossiers', parameters=parameters)