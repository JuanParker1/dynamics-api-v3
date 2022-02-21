"""
Kairnial controls module models
"""
import hashlib
import json
import os

from django.core.files.uploadedfile import InMemoryUploadedFile

from dynamics_apis.common.models import PaginatedModel
from dynamics_apis.controls.services import KairnialControlInstanceService, KairnialControlTemplateService


class ControlTemplate(PaginatedModel):
    """
    Kairnial Control template
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
        kf = KairnialControlTemplateService(client_id=client_id, token=token, project_id=project_id)
        return kf.list(parent_id=parent_id, filters=filters).get('brut')