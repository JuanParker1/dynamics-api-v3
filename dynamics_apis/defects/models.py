"""
Kairnial defect models
"""
from dynamics_apis.authorization.models import ACL
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
        :param page_offset: start pagination at given offset
        :param page_limit: number of records
        :return:
        """
        transmitter = [e.get('label') for e in ACL.transmitters(
            client_id=client_id,
            token=token,
            project_id=project_id,
            user_id=user_id)]
        if 'emetteurs' not in filters:
            filters['emetteurs'] = transmitter
        kf = KairnialDefectService(client_id=client_id, token=token, project_id=project_id,
                                   user_id=user_id)
        defects = kf.list(filters=filters, limit=page_limit, offset=page_offset)
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
        kf = KairnialDefectService(client_id=client_id, token=token, project_id=project_id,
                                   user_id=user_id)
        results = kf.get(pk)
        print(results)
        try:
            total = int(results.get('total'))
        except ValueError:
            total = 0
        if total:
            try:
                return results.get('pins')[0]
            except IndexError:
                return None
        else:
            return None

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
        return levels
