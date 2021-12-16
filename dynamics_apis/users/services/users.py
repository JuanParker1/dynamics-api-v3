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
            action='getUsers',
            use_cache=True)

    def get(self, pk) -> []:
        """
        Get user using getFilteredUser
        """
        return self.call(
            action='getFilteredUser',
            parameters=[{'userIdList': [pk, ]}],
            use_cache=True)

    def list_for_groups(self, list_of_groups: [str]) -> []:
        """
        List users for a set of given groups.
        Having no group will return an empty set
        :param list_of_groups: List of group IDs
        :return:
        """
        return self.call(
            action='getUsersByGroup',
            parameters=[{'groupList': list_of_groups}],
            use_cache=True)

    def get_groups(self, pk):
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
        return self.call(
            service='aclmanager',
            action='inviteUsers',
            parameters=users,
            use_cache=False
        )