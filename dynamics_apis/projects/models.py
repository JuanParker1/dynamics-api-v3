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
        :param project_id: Project RGOC Code
        :param search: Search on project name
        :return:
        """
        kp = KairnialProject(client_id=client_id, token=token)
        projects = kp.list(search=search).get('items')
        return projects