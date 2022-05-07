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
            filters: dict = None,
            user_id: str = None
    ):
        """
        List defects
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param filters: serialized values from a DefectQuerySerializer
        :param user_id: ID of the user
        :return:
        """
        kf = KairnialDefectService(client_id=client_id, token=token, project_id=project_id, user_id=user_id)
        defects = kf.list(filters=filters, limit=page_limit, offset=page_offset)
        print(defects)
        return defects

    @staticmethod
    def get(
            client_id: str,
            token: str,
            project_id: str,
            pk: int,
            user_id: str = None
    ):
        """
        Get a specific defect by numeric ID
        """
        kf = KairnialDefectService(client_id=client_id, token=token, project_id=project_id, user_id=user_id)
        return kf.get(pk)

    @staticmethod
    def create(
            client_id: str,
            token: str,
            project_id: str,
            serialized_data: dict,
            user_id: str = None
    ):
        """
        Create a Kairnial Defect
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param serialized_data: DefectCreateSerializer validated data
        :param user_id: ID of the user
        :return: DefectSerializer data
        """
        ds = KairnialDefectService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id)
        return ds.create(defect_create_serializer=serialized_data)

    @staticmethod
    def areas(client_id: str,
              token: str,
              project_id: str,
              user_id: str = None):
        """
        List defect areas
        Create a Kairnial Defect
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param user_id: ID of the user
        :return: DefectAreaSerializer data
        """
        ds = KairnialDefectService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id)
        areas = ds.areas()
        print(areas)
        return areas

    @staticmethod
    def bim_categories(client_id: str,
                       token: str,
                       project_id: str,
                       user_id: str = None):
        """
        List defect BIM categories
        Create a Kairnial Defect
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param user_id: ID of the user
        :return: DefectBIMCategorySerializer data
        """
        ds = KairnialDefectService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id)
        categories = ds.bim_categories()
        print(categories)
        return categories

    @staticmethod
    def bim_levels(client_id: str,
                   token: str,
                   project_id: str,
                   user_id: str = None):
        """
        List defect BIM levels
        Create a Kairnial Defect
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param user_id: ID of the user
        :return: DefectBIMCategorySerializer data
        """
        ds = KairnialDefectService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id)
        levels = ds.bim_levels()
        print(levels)
        return levels
