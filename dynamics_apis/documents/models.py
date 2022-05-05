"""
Kairnial Files module models
"""
import hashlib
import json
import os

from django.core.files.uploadedfile import InMemoryUploadedFile

from dynamics_apis.common.models import PaginatedModel
from dynamics_apis.documents.services import KairnialFolderService, KairnialDocumentService, \
    KairnialApprovalTypeService, KairnialApprovalService


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
            user_id: str = None
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param parent_id: ID of the parent folder
        :param filters: Dictionary of filters
        :param user_id: ID of the user
        :return:
        """
        kf = KairnialFolderService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        folder_list = kf.list(parent_id=parent_id, filters=filters).get('brut')
        print("before filter", folder_list)
        if 'path' in filters:
            output = []
            for folder in folder_list:
                if folder.get('fcat_chemin').lower().startswith(filters['path'].lower()):
                    output.append(folder)
            folder_list = output
        print("after path filter", folder_list)
        if 'exact_path' in filters:
            output = []
            for folder in folder_list:
                if folder.get('fcat_chemin').lower().startswith(filters['exact_path'].lower()):
                    output.append(folder)
            folder_list = output
        print("after exact_path filter", folder_list)
        if 'name' in filters:
            output = []
            for folder in folder_list:
                if folder.get('originalName').lower().startswith(filters['name'].lower()):
                    output.append(folder)
            folder_list = output
        print("after name filter", folder_list)
        return folder_list

    @staticmethod
    def get(
            client_id: str,
            token: str,
            project_id: str,
            id: int,
            user_id: str = None
    ):
        """
        Get Folder by ID
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param id: Numeric ID of the folder
        :param user_id: ID of the user
        """
        kf = KairnialFolderService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return kf.get(id=id)

    @staticmethod
    def create(
            client_id: str,
            token: str,
            project_id: str,
            serialized_data: dict,
            user_id: str = None
    ):
        """
        Create a Kairnial Folder
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param serialized_data: FolderCreateSerializer validated data
        :param user_id: ID of the user
        :return: FolderSerializer data
        """
        fs = KairnialFolderService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return fs.create(folder_create_serializer=serialized_data)

    @staticmethod
    def update(
            client_id: str,
            token: str,
            project_id: str,
            id: int,
            serialized_data: dict,
            user_id: str = None
    ):
        """
        Update a Kairnial Folder
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param id: Numeric ID of the folder
        :param serialized_data: FolderUpdateSerializer validated data
        :param user_id: ID of the user
        """
        fs = KairnialFolderService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return fs.update(id=id, folder_update_serializer=serialized_data)

    @staticmethod
    def archive(
            client_id: str,
            token: str,
            project_id: str,
            id: str,
            user_id: str = None
    ):
        """
        Archive a Kairnial Folder
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param id: Universal ID of the folder
        :param user_id: ID of the user
        """
        fs = KairnialFolderService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
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
            filters: dict = None,
            user_id: str = None
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param parent_id: ID of the parent folder
        :param filters: Dictionary of filters
        :param user_id: ID of the user
        :return:
        """
        kf = KairnialDocumentService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return kf.list(parent_id=parent_id, filters=filters).get('fichiers')

    @staticmethod
    def get(
            client_id: str,
            token: str,
            project_id: str,
            id: int,
            user_id: str = None
    ):
        """
        Get Document by ID
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param id: Numeric ID of the document
        :param user_id: ID of the user
        """
        kf = KairnialDocumentService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return kf.get(id=id)

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
            attachment,
            user_id: str = None
    ):
        """
        Create a Kairnial Document
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param serialized_data: DocumentCreateSerializer validated data
        :param attachment: File field
        :param user_id: ID of the user
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
        fs = KairnialDocumentService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return fs.create(document_create_serializer=serialized_data, content=file_content)

    @classmethod
    def update(
            cls,
            client_id: str,
            token: str,
            project_id: str,
            parent_id: str,
            serialized_data: dict,
            attachment,
            user_id: str = None
    ):
        """
        Revise a Kairnial Document
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param serialized_data: DocumentCreateSerializer validated data
        :param attachment: File field
        :param user_id: ID of the user
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
        serialized_data['parentUUID'] = parent_id
        fs = KairnialDocumentService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return fs.revise(document_revise_serializer=serialized_data, content=file_content)

    @staticmethod
    def archive(
            client_id: str,
            token: str,
            project_id: str,
            id: int,
            user_id: str = None
    ):
        """
        Archive a Kairnial Document
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param id: Numeric ID of the document
        """
        fs = KairnialDocumentService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id)
        return fs.archive(id=id)

    @staticmethod
    def check_revision(
            client_id: str,
            token: str,
            project_id: str,
            document_serialized_data: dict,
            supplementary_serialized_data: dict,
            user_id: str = None
    ):
        """
        Create a Kairnial Document
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param document_serialized_data: DocumentSearchRevisionSerializer validated data
        :param supplementary_serialized_data: DocumentSearchRevisionSupplementaryArguments validated data
        :param user_id: ID of the user
        :return: DocumentSerializer data
        """
        fs = KairnialDocumentService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return fs.check_revision(
            document_search_revision_serializer=document_serialized_data,
            supplementary_info_serializer=supplementary_serialized_data
        ).get('').get('')



class ApprovalType(PaginatedModel):

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            user_id: str = None
    ):
        """
        List document approval types
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :return:
        """
        kat = KairnialApprovalTypeService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id
        )
        approval_types = kat.list().get('notes')
        for at in approval_types:
            at['content'] = json.loads(at.get('content') or '{}')
        return approval_types

    @staticmethod
    def archive(
            client_id: str,
            token: str,
            project_id: str,
            id: int,
            user_id: str = None,
    ):
        """
        Archive a Kairnial Approval type
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param id: Numeric ID of the approval type
        """
        ats = KairnialApprovalTypeService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id
        )
        return ats.archive(id=id)


class Approval(PaginatedModel):
    """
    Model for document approval
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            user_id: str = None
    ):
        """
        List document approval types
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param user_id: Optional User ID
        :return:
        """
        output = []
        ka = KairnialApprovalService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id)
        for fileid, list_of_approvals in ka.list().get('visas').items():
            output.extend(list_of_approvals)
        return output

    @staticmethod
    def update(
            client_id: str,
            token: str,
            project_id: str,
            document_id,
            workflow_id,
            approval_id,
            new_status,
            user_id: str = None
    ) -> [int, int, bool]:
        """
        Archive existing approval step and create a new step
        :param client_id: ID of the client
        :param token: access token
        :param project_id: Project RGOC
        :param document_id: Numeric ID of the document
        :param workflow_id: Numeric ID of the workflow
        :param approval_id: Numeric ID of the approval
        :param new status: Numeric ID of the approval step
        return: [Approval ID, Step ID, ok?]
        """
        ka = KairnialApprovalService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id
        )
        return ka.update(
            document_id=document_id,
            workflow_id=workflow_id,
            approval_id=approval_id,
            new_status=new_status)
