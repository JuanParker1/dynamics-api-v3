"""
Kairnial group model classes
"""
from dynamics_apis.users.services.groups import KairnialGroup


class Group:
    """
    Kairnial Group class
    """
    name = None
    description = None
    properties = {
        'name': 'groups_label',
        'description': 'groups_description'
    }
    filters = ['name', ]

    def __init__(self, name: str, description: str = ''):
        self.name = name
        self.description = description

    @classmethod
    def list(cls, client_id: str, token: str, project_id: str, filters: dict = {}) -> []:
        """
        Get a filtered list of groups from web services
        """
        kg = KairnialGroup(client_id=client_id, token=token, project_id=project_id)
        groups = kg.list().get('groups')
        manual_filters = (set(cls.filters) & set(filters.keys())) or []
        for m in manual_filters:
            groups = [g for g in groups if filters.get(m).lower() in g.get(cls.properties[m], '').lower()]
        return groups

    def create(self, client_id: str, token: str, project_id: str):
        """
        Create a group through Kairnial Web services call
        """
        kg = KairnialGroup(client_id=client_id, token=token, project_id=project_id)
        return kg.create(self)

    @staticmethod
    def add_users(client_id: str, token: str, project_id: str, pk: int, user_list: [str]):
        """
        Add user to group
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param pk: Group numeric ID
        :user_id: List of user numeric ID
        """
        kg = KairnialGroup(client_id=client_id, token=token, project_id=project_id)
        return kg.add_users(group_id=pk, user_list=user_list)

    @staticmethod
    def remove_users(client_id: str, token: str, project_id: str, pk: int, user_list: [str]):
        """
        Add user to group
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param pk: Group numeric ID
        :user_id: List of user numeric ID
        """
        kg = KairnialGroup(client_id=client_id, token=token, project_id=project_id)
        return kg.remove_users(group_id=pk, user_list=user_list)



