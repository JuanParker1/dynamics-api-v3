"""
Call to Kairnial Group Web Services
"""
from dynamics_apis.common.services import KairnialWSService

GROUP_LIST_PATH = 'users.getGroups'


class KairnialGroup(KairnialWSService):
    """
    Service class for Kairnial Groups
    """
    service_domain = 'users'

    def list(self) -> []:
        """
        List users
        :return:
        """
        return self.call(action='getGroups', parameters=[{'allGroups': True}])

    def create(self, group):
        """
        Create a group through Kairnial Web Services
        :param group: dynamics_apis.users.models.Group
        """
        return self.call(action='addGroup', parameters=[group.name, group.description], format='bool')

    def add_users(self, group_id: int, user_list: [int]):
        """
        Add a list of users to a group
        """
        no_error = True
        for user in user_list:
            resp = self.call(action='addUserToGroup', parameters=[{'groupe': group_id, 'user': [user, ]}],
                             format='bool')
            no_error &= resp
        return no_error

    def remove_users(self, group_id: int, user_list: [int]):
        """
        Add a list of users to a group
        """
        no_error = True
        for user in user_list:
            resp = self.call(action='removeUserFromGroup', parameters=[{'groupe': group_id, 'user': [user, ]}],
                             format='bool')
            no_error &= resp
        return no_error
