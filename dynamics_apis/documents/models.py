"""
Kairnial Files module models
"""
from dynamics_apis.documents.services import FolderService
from dynamics_apis.common.models import PaginatedModel

class Folder(PaginatedModel):
    """
    Kairnial Dossier
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            parent_id: str = None,
            filters: dict = None,
            page_number: int = 0,
            page_size: int = 100
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param parent_id: ID of the parent folder
        :return:
        """
        kf = FolderService(client_id=client_id, token=token, project_id=project_id)
        return kf.list(parent_id=parent_id, filters=filters).get('brut')

    @staticmethod
    def get(
            client_id: str,
            token: str,
            project_id: str,
            id: int
    ):
        """
        Get Folder by ID
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param id: Numeric ID of the folder
        """
        kf = FolderService(client_id=client_id, token=token, project_id=project_id)
        return kf.get(id=id)



class Document:
    """
    Kairnial File
    """

    @staticmethod
    def list(client_id: str, token: str, project_id: str, folder_id: str):
        """
        List documents in a folder
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param folder_id: ID of the parent folder
        :return:
        """
        pass
