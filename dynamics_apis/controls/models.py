"""
Kairnial controls module models
"""

from dynamics_apis.common.models import PaginatedModel
from dynamics_apis.controls.services import KairnialControlTemplateService, KairnialControlInstanceService


class ControlTemplate(PaginatedModel):
    """
    Kairnial Control template
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            page_offset: int,
            page_limit: int,
            filters: dict = None
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param filters: serialized values from a
        :return:
        """
        kf = KairnialControlTemplateService(client_id=client_id, token=token, project_id=project_id)
        return kf.list(filters=filters, limit=page_limit, offset=page_offset)


class ControlInstance(PaginatedModel):
    """
    Kairnial Control instances
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            page_offset: int,
            page_limit: int,
            filters: dict = None
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :return:
        """
        kf = KairnialControlInstanceService(client_id=client_id, token=token, project_id=project_id)
        return kf.list(filters=filters, limit=page_limit, offset=page_offset)
