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