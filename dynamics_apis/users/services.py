"""
Call to Kairnial Web Services
"""
from dynamics_apis.common.services import KairnialWSService

USER_LIST_SERVICE = 'users.getUsers'
USER_COUNT_SERVICE = 'users.getNbUsers'

GROUP_LIST_PATH = 'users.getGroups'


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
        response = self.call(action='getNbUsers')

    def list(self, project: str = None) -> []:
        """
        List users
        :return:
        """
        response = self.call(action='getUsers')
