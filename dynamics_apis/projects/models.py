"""
Kairnial user model classes
"""
import json

from dynamics_apis.authorization.models import Module
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
        Get a list of projects
        :param client_id: ClientID Token
        :param token: Access token
        :param search: Search on project name
        :return:
        """
        kp = KairnialProject(client_id=client_id, token=token)
        return kp.list(search=search, page_offset=page_offset, page_limit=page_limit)

    @classmethod
    def integration_list(cls, client_id: str, token: str, search: str, page_offset: int, page_limit: int):
        """
        Get a list of projects for integration into Atrium
        :param client_id: ClientID Token
        :param token: Access token
        :param search: Search on project name
        :return:
        """
        kp = KairnialProject(client_id=client_id, token=token)
        project_list = kp.list(search=search, page_offset=page_offset, page_limit=page_limit)
        output = []
        total = project_list.get('total')
        page_offset = project_list.get('LIMITSKIP')
        page_limit = project_list.get('LIMITTAKE')
        for project in project_list.get('items'):
            print(project)
            km = Module.list(client_id=client_id, token=token, project_id=project.get('g_nom'))
            try:
                info = json.loads(project.get('g_infos'))
                project['cover_image_url'] = info.get('picture')
            except json.JSONDecodeError:
                project['cover_image_url'] = ''
            metadata = {
                'project_code': project.get('g_nom'),
                'modules': km
            }
            print("metadata", metadata)
            project['meta_data'] = metadata
            output.append(project)
        print(output)
        return total, output, page_offset, page_limit


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
