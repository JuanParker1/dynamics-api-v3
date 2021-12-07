"""
Call to Kairnial Web Services
"""
import json
from hashlib import sha1

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext as _
from dynamics_apis.authentication.services import KairnialAuthentication
from dynamics_apis.common.services import KairnialWSServiceError

PROJECT_LIST_PATH = '/api/v2/projects'


class KairnialProject:
    """
    Service class for Kairnial Pojects
    """
    client_id = None
    token = None
    token_type = None


    def __init__(self, client_id: str, token: str, token_type='Bearer'):
        """
        Initialize the project fecthing library
        :param token: Access token to pass to header
        """
        self.client_id = client_id
        self.token = token
        self.token_type = token_type

    @classmethod
    def from_authenticator(cls, authenticator: KairnialAuthentication):
        """
        Initiate a KairnialProject from KairnialAuthentication
        :param authenticator: KairnialAuthentication
        :return:
        """
        return cls(
            client_id=authenticator.client_id,
            token=authenticator.token,
            token_type=authenticator.token_type
        )

    def list(self, search: str = None) -> []:
        """
        List projects
        :return:
        """
        url = settings.KAIRNIAL_AUTH_SERVER + PROJECT_LIST_PATH
        data = {
            'client_id': self.client_id,
            'LIMITSKIP': 0,
            'LIMITTAKE': 1000,
            'onlyUUID': False
        }
        if search:
            data['SEARCH'] = search
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'{self.token_type} {self.token}'
        }
        cache_key = sha1(f'{url}||{json.dumps(headers)}||{data}'.encode('latin1')).hexdigest()
        if cache.get(cache_key):
            return cache_key
        response = requests.post(
            url,
            headers=headers,
            data=data
        )
        if response.status_code != 200:
            raise KairnialWSServiceError(
                message=_(f"Fetching from Kairnial backend failed with response {response.status_code}: {response.content}"),
                status=response.status_code
            )
        json_response = response.json()
        cache.set(cache_key, json_response)
        return json_response

