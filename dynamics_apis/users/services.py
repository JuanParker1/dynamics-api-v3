"""
Call to Kairnial Web Services
"""
import requests
from django.conf import settings
from django.utils.translation import ugettext as _
from dynamics_apis.common.models import KairnialServiceError

PROJECT_LIST_PATH = 'https://ws-support.kairnial.io/user/5cfaa212facaaa0fc2e10eb53c9118e92092b495cd17127080e7d61dd4ac477b/users.getGroups'
USER_LIST_SERVICE = 'users.getUsers'

class KairnialUser:
    """
    Service class for Kairnial Pojects
    """

    def __init__(self, client_id: str, token: str):
        """
        Initialize the project fecthing library
        :param token: Access token to pass to header
        """
        self.client_id = client_id
        self.token = token

    def list(self, search: str = None) -> []:
        """
        List projects
        :return:
        """
        payload = {
            'client_id': self.client_id,
            'LIMITSKIP': 0,
            'LIMITTAKE': 1000,
            'onlyUUID': False
        }
        if search:
            payload['SEARCH'] = search
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.post(
            settings.KAIRNIAL_AUTH_SERVER + PROJECT_LIST_PATH,
            headers=headers,
            data=payload
        )
        if response.status_code != 200:
            raise KairnialServiceError(
                _(f"Fetching from Kairnial backend failed with response {response.status_code}: {response.content}"))
        return response.json()
