"""
Kairnial Files module models
"""
import hashlib
import os
from django.core.files.uploadedfile import InMemoryUploadedFile

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

    @classmethod
    def extract_attachment_data(cls, attachment: InMemoryUploadedFile):
        """
        Read attributes from InMemoryUploadFile object
        """
        name = os.path.splitext(attachment.name)[0]
        extension = os.path.splitext(attachment.name)[-1][1:]
        file_type = attachment.content_type
        file_handler = attachment.file
        file_content = attachment.read()
        file_hash = hashlib.md5(file_content).hexdigest()
        file_size = attachment.size
        print(name, extension, file_type, file_handler, file_hash, file_size)
        return name, extension, file_type, file_handler, file_hash, file_size, file_content

    @classmethod
    def create(
            cls,
            client_id: str,
            token: str,
            project_id: str,
            serialized_data: dict,
            attachment
    ):
        """
        Create a Kairnial Document
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param serialized_data: DocumentCreateSerializer validated data
        :return: DocumentSerializer data
        """
        name, extension, \
        file_type, \
        file_handler, \
        file_hash, \
        file_size, \
        file_content = cls.extract_attachment_data(
            attachment=attachment
        )
        if 'nom' not in serialized_data:
            serialized_data['nom'] = name
        serialized_data['ext'] = extension
        serialized_data['hash'] = file_hash
        serialized_data['size'] = file_size
        serialized_data['typeFichier'] = file_type
        fs = KairnialDocumentService(client_id=client_id, token=token, project_id=project_id)
        return fs.create(document_create_serializer=serialized_data, content=file_content)
