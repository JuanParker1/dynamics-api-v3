"""
Call to Kairnial Web Services
"""
from dynamics_apis.common.services import KairnialWSService


class KairnialContact(KairnialWSService):
    """
    Service class for Kairnial Contacts
    """
    service_domain = 'contacts'
    item_type='contact'

    def list(self, parameters=[{}, ]) -> []:
        """
        List contacts
        :param search: Search contact
        :return:
        """
        return self.call(action='getItem', parameters=parameters)
