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
            cache=True
        )

    def list(self) -> []:
        """
        List users
        :return:
        """
        return self.call(
            action='getUsers',
            cache=True)

    def get(self, pk) -> []:
        """
        Get user using getFilteredUser
        """
        return self.call(
            action='getFilteredUser',
            parameters=[{'userIdList': [pk, ]}],
            cache=True)

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
            cache=True)
