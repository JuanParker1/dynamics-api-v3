"""
Kairnial user model classes
"""
from dynamics_apis.common.models import PaginatedModel
from dynamics_apis.projects.services import KairnialProject


# Create your models here.
class Project(PaginatedModel):
    """
    Kairnial project class
    """

    @classmethod
    def list(cls, client_id: str, token: str, search: str, page_offset: int, page_limit: int,
             **kwargs) -> []:
        """
        Get a list of users for a project
        :param client_id: ClientID Token
        :param token: Access token
        :param search: Search on project name
        :param page_offset: # of first record
        :page_limit: max nb of records per request
        :return:
        """
        kp = KairnialProject(client_id=client_id, token=token)
        return kp.list(search=search, page_offset=page_offset, page_limit=page_limit)

    @classmethod
    def create(cls, client_id: str, token: str, serialized_project):
        """
        Create a new project
        :param client_id: ClientID Token
        :param token: Access token
        :param serialized_project: ProjectCreationSerializer validated_date
        """
        kp = KairnialProject(client_id=client_id, token=token)
        return kp.create(serialized_project=serialized_project)

    @classmethod
    def update(cls, client_id: str, token: str, pk: str, serialized_project):
        """
        Update an existing project
        :param client_id: ClientID Token
        :param token: Access token
        :param pk: RGOC ID of the project
        :param serialized_project: ProjectUpdateSerializer validated_date
        :return:
        """
        kp = KairnialProject(client_id=client_id, token=token)
        return kp.update(pk=pk, serialized_update_project=serialized_project)
