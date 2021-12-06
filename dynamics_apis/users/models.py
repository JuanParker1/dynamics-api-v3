"""
Kairnial user model classes
"""
from dynamics_apis.users.services.groups import KairnialGroup
from dynamics_apis.users.services.users import KairnialUser


# Create your models here.
class User:
    """
    Kairnial user class
    """
    properties = {
        'email': 'account_email',
        'full_name': 'account_firstname',
        'archived': 'account_archive'
    }
    filters = ['email', 'full_name']
    @classmethod
    def list(cls, client_id: str, token: str, project_id: str, filters: dict = {}) -> []:
        """
        Get a list of users for a project
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param filters: Dict of filters
        :return:
        """
        ku = KairnialUser(client_id=client_id, token=token, project_id=project_id)
        if 'groups' in filters:
            try:
                list_of_groups = [int(a.strip()) for a in filters.get('groups').split(',') if a]
                print(list_of_groups)
                users = ku.list_for_groups(list_of_groups=list_of_groups)
            except ValueError as e:
                print(e)
                return None
        else:
            users = ku.list().get('users')
        manual_filters = set(filters.keys()) & set(cls.filters)
        for m in manual_filters:
            users = [u for u in users if filters.get(m).lower() in u.get(cls.properties[m]).lower()]
        if 'archived' in filters:
            users = [u for u in users if getattr(u, 'account_archive', 0) == 0]
        return users

    @classmethod
    def count(cls, client_id: str, token: str, project_id: str):
        """
        Get a count of users on the project
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        """
        ku = KairnialUser(client_id=client_id, token=token, project_id=project_id)
        return ku.count()


    @classmethod
    def get(cls, client_id: str, token: str, project_id: str, pk: str):
        """
        Get a specific user
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param pk: Group numeric ID
        """
        ku = KairnialUser(client_id=client_id, token=token, project_id=project_id)
        return ku.get(pk=pk)



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



