"""
Kairnial defect models
"""

from dynamics_apis.common.models import PaginatedModel
from dynamics_apis.defects.services import KairnialDefectService


class Defect(PaginatedModel):
    """
    Kairnial Defect
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
        List defects
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param filters: serialized values from a DefectQuerySerializer
        :return:
        """
        kf = KairnialDefectService(client_id=client_id, token=token, project_id=project_id)
        return kf.list(filters=filters, limit=page_limit, offset=page_offset)

