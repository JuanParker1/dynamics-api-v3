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
        :param filters: serialized values from a ControlTemplateQuerySerializer
        :return:
        """
        kf = KairnialControlTemplateService(client_id=client_id, token=token, project_id=project_id)
        return kf.list(filters=filters, limit=page_limit, offset=page_offset)


class ControlTemplateContent(PaginatedModel):
    """
    Kairnial Control template
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            template_id: str
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param template_id: UUID of the template to fetch
        :return:
        """
        kf = KairnialControlTemplateService(client_id=client_id, token=token, project_id=project_id)
        if template:=kf.list(filters={'template_uuid': template_id}):
            return template[0].get('content')
        return None


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
