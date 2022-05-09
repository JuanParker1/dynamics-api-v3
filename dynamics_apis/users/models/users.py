"""
Kairnial user model classes
"""
from dynamics_apis.users.services.users import KairnialUser


class UserNotFound(Exception):
    msg = 'User not found'


# Create your models here.
class User:
    """
    Kairnial user class
    """

    @classmethod
    def list(cls, client_id: str, token: str, project_id: str, filters: dict = dict, user_id: str = None) -> []:
        """
        Get a list of users for a project
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param filters: Dict of filters
        :param user_id: Optional ID of the user
        :return:
        """
        ku = KairnialUser(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        if 'groups' in filters:
            try:
                users = ku.list_for_groups(list_of_groups=filters.get('groups'))
            except ValueError:
                return None
        else:
            users = ku.list().get('items')
        for key, value in filters.items():
            if type(value) == str:
                users = [u for u in users if value.lower() in u.get(key, "").lower()]
            elif type(value) == bool or type(value) == int:
                users = [u for u in users if value == u.get(key)]
        return users

    @classmethod
    def count(cls, client_id: str, token: str, project_id: str, user_id: str = None):
        """
        Get a count of users on the project
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param user_id: Optional ID of the user
        """
        ku = KairnialUser(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return ku.count()

    @classmethod
    def get(cls, client_id: str, token: str, project_id: str, pk: str, user_id: str = None):
        """
        Get a specific user
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param pk: User UUID
        :param user_id: Optional ID of the user
        """
        ku = KairnialUser(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        user_list = ku.list().get('items')
        try:
            return [user for user in user_list if user.get('account_uuid') == pk][0]
        except IndexError:
            raise UserNotFound('User not found')

    @classmethod
    def groups(
            self,
            client_id: str,
            token: str,
            project_id: str,
            pk: int,
            user_id: str = None):
        """
        Get a specific user
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param pk: Group numeric ID
        :param user_id: Optional ID of the user
        """
        ku = KairnialUser(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return ku.get_groups(pk=pk)

    @classmethod
    def invite(self, client_id: str, token: str, project_id: str, users: list, user_id: str = None):
        """
        Get a specific user
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param users: List of validated UserInviteSerializer
        :param user_id: Optional ID of the user
        """
        ku = KairnialUser(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id
        )
        return ku.invite(users=users)

    @classmethod
    def archive(self,
                client_id: str,
                token: str,
                project_id: str,
                pk: str,
                user_id: str = None):
        """
        Archive a user
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param pk: User UUID
        :param user_id: Optional ID of the user
        """
        ku = KairnialUser(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id)
        return ku.archive(pk=pk)
