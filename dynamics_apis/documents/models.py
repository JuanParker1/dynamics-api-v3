"""
Kairnial Files module models
"""
from dynamics_apis.common.models import PaginatedModel
from dynamics_apis.documents.services import KairnialFolderService, KairnialDocumentService


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
            filters: dict = None
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param parent_id: ID of the parent folder
        :return:
        """
        kf = KairnialFolderService(client_id=client_id, token=token, project_id=project_id)
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
        kf = KairnialFolderService(client_id=client_id, token=token, project_id=project_id)
        return kf.get(id=id)

    @staticmethod
    def create(
            client_id: str,
            token: str,
            project_id: str,
            serialized_data: dict
    ):
        """
        Create a Kairnial Folder
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param serialized_data: FolderCreateSerializer validated data
        :return: FolderSerializer data
        """
        fs = KairnialFolderService(client_id=client_id, token=token, project_id=project_id)
        return fs.create(folder_create_serializer=serialized_data)

    @staticmethod
    def update(
            client_id: str,
            token: str,
            project_id: str,
            id: int,
            serialized_data: dict
    ):
        """
        Update a Kairnial Folder
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param id: Numeric ID of the folder
        :param serialized_data: FolderUpdateSerializer validated data
        """
        fs = KairnialFolderService(client_id=client_id, token=token, project_id=project_id)
        return fs.update(id=id, folder_update_serializer=serialized_data)

    @staticmethod
    def archive(
            client_id: str,
            token: str,
            project_id: str,
            id: int,
    ):
        """
        Archive a Kairnial Folder
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param id: Universal ID of the folder
        """
        fs = KairnialFolderService(client_id=client_id, token=token, project_id=project_id)
        return fs.archive(id=id)


class Document(PaginatedModel):
    """
    Kairnial File
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            parent_id: str = None,
            filters: dict = None
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param parent_id: ID of the parent folder
        :return:
        """
        kf = KairnialDocumentService(client_id=client_id, token=token, project_id=project_id)
        return kf.list(parent_id=parent_id, filters=filters).get('fichiers')

    @staticmethod
    def create(
            client_id: str,
            token: str,
            project_id: str,
            serialized_data: dict
    ):
        """
        Create a Kairnial Document
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param serialized_data: DocumentCreateSerializer validated data
        :return: DocumentSerializer data
        """
        fs = KairnialDocumentService(client_id=client_id, token=token, project_id=project_id)
        return fs.create(folder_create_serializer=serialized_data)
