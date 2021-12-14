"""
Kairnial user model classes
"""
from dynamics_apis.users.services.groups import KairnialGroup
from dynamics_apis.projects.services import KairnialProject


# Create your models here.
class Project:
    """
    Kairnial project class
    """
    properties = {
        'name': 'rgoc_desc',
    }
    filters = ['name', ]
    @classmethod
    def list(cls, client_id: str, token: str, search: str) -> []:
        """
        Get a list of users for a project
        :param client_id: ClientID Token
        :param token: Access token
        :param search: Search on project name
        :return:
        """
        kp = KairnialProject(client_id=client_id, token=token)
        projects = kp.list(search=search).get('items')
        return projects

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