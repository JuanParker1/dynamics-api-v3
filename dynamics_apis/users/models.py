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
        :param client_id:
        :param token:
        :param project:
        :param filters: Dict of filters
        :return:
        """
        ku = KairnialUser(client_id=client_id, token=token, project_id=project_id)
        if 'groups' in filters:
            try:
                list_of_groups = [int(a.strip()) for a in filters.get('groups').split(',')]
                users = ku.list_for_groups(list_of_groups=list_of_groups)
            except ValueError:
                return None
        else:
            users = ku.list().get('users')
        print(filters)
        manual_filters = set(filters.keys()) & set(cls.filters)
        for m in manual_filters:
            users = [u for u in users if filters.get(m).lower() in u.get(cls.properties[m]).lower()]
        if 'archived' in filters:
            users = [u for u in users if getattr(u, 'account_archive', 0) == 0]
        return users


class Group:
    """
    Kairnial Group class
    """
    properties = {
        'name': 'groups_label',
        'description': 'groups_description'
    }
    filters = ['name', ]
    @classmethod
    def list(cls, client_id: str, token: str, project_id: str, filters: dict = {}) -> []:
        kg = KairnialGroup(client_id=client_id, token=token, project_id=project_id)
        groups = kg.list().get('groups')
        manual_filters = (set(cls.filters) & set(filters.keys())) or []
        for m in manual_filters:
            groups = [g for g in groups if filters.get(m).lower() in g.get(cls.properties[m], '').lower()]
        return groups

