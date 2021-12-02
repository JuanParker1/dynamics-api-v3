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
