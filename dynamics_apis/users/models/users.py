"""
Kairnial user model classes
"""
from dynamics_apis.users.services.groups import KairnialGroup
from dynamics_apis.users.services.users import KairnialUser


class UserNotFound(Exception):
    msg = 'User not found'


# Create your models here.
class User:
    """
    Kairnial user class
    """
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
                users = ku.list_for_groups(list_of_groups=filters.get('groups'))
            except ValueError as e:
                return None
        else:
            users = ku.list().get('items')
        for key, value in filters.items():
            if value == str:
                users = [u for u in users if value.lower() in u.get(key).lower()]
            elif value is bool or value is int:
                users = [u for u in users if value == u.get(key)]
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
        try:
            return [user for user in ku.list() if user.get('account_uuid') == pk][0]
        except IndexError as e:
            raise UserNotFound('User not found')

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

