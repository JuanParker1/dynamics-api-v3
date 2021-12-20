"""
Kairnial Files module models
"""
from dynamics_apis.documents.services import FolderService


class Folder:
    """
    Kairnial Dossier
    """

    @staticmethod
    def list(client_id: str, token: str, project_id: str, parent_id: str=None, filters: dict = None):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param parent_id: ID of the parent folder
        :return:
        """
        kf = FolderService(client_id=client_id, token=token, project_id=project_id)
        return kf.list(parent_id=parent_id, filters=filters)


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