"""
Call to Kairnial Web Services
"""
from dynamics_apis.common.services import KairnialWSService


class KairnialUser(KairnialWSService):
    """
    Service class for Kairnial Pojects
    """
    service_domain = 'users'

    def count(self):
        """
        Count users on a project
        :return:
        """
        return self.call(
            action='getNbUsers',
            use_cache=True
        )

    def list(self) -> []:
        """
        List users
        :return:
        """
        return self.call(
            service='aclmanager',
            action='getUsers',
            use_cache=True)


    def list_for_groups(self, list_of_groups: []) -> []:
        """
        List users for a set of given groups.
        Having no group will return an empty set
        :param list_of_groups: List of group IDs
        :return:
        """
        parameters = [{'groupList': {el: True for el in list_of_groups}}]
        return self.call(
            action='getUsersByGroup',
            parameters=parameters,
            use_cache=True)

    def get_groups(self, pk: int):
        """
        Get groups for user
        :param pk: User Numeric ID
        :return:
        """
        return self.call(
            action='getUserGroups',
            parameters=[pk,],
            use_cache=True
        )

    def invite(self, users: []):
        """
        Invite now users
        :param users: list of UserInviteSerializer validated_data
        :return:
        """
        invited_users = []
        for user in users:
            response = self.call(
                service='aclmanager',
                action='inviteUser',
                parameters=[user],
                use_cache=False
            )
            if response.get('success'):
                invited_users.append(response)
        return invited_users

    def archive(self, pk: str):
        """
        Archive user on project
        :param pk: User UUID
        :return:
        """
        return self.call(
            service='aclmanager',
            action='archiveUser',
            parameters=[{'account_uuid': pk}],
            use_cache=False
        )