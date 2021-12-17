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
    def list(cls, client_id: str, token: str, project_id: str, filters: dict = dict) -> []:
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
                users = ku.list_for_groups(list_of_groups=list_of_groups)
            except ValueError as e:
                return None
        else:
            users = ku.list().get('items')
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
        :param pk: User UUID
        """
        ku = KairnialUser(client_id=client_id, token=token, project_id=project_id)
        return [user for user in ku.get(pk=pk) if user.get('account_uuid') == pk]

    @classmethod
    def groups(self, client_id: str, token: str, project_id: str, pk: int):
        """
        Get a specific user
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param pk: Group numeric ID
        """
        ku = KairnialUser(client_id=client_id, token=token, project_id=project_id)
        return ku.get_groups(pk=pk)

    @classmethod
    def invite(self, client_id: str, token: str, project_id: str, users: list):
        """
        Get a specific user
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param users: List of validated UserInviteSerializer
        """
        ku = KairnialUser(client_id=client_id, token=token, project_id=project_id)
        return ku.invite(users=users)

    @classmethod
    def archive(self, client_id: str, token: str, project_id: str, pk: str):
        """
        Archive a user
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param pk: User UUID
        """
        ku = KairnialUser(client_id=client_id, token=token, project_id=project_id)
        return ku.archive(pk=pk)