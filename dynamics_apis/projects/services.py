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
from dynamics_apis.common.services import KairnialWSServiceError, KairnialCrossService

PROJECT_LIST_PATH = '/api/v2/projects'
PROJECT_CREATION_PATH = '/adminEC'

class KairnialProject(KairnialCrossService):
    """
    Service class for Kairnial Pojects
    """
    service_domain = 'gadmin_projects'
    client_id = None
    token = None
    token_type = None

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

    def create(self, name: str):
        """
        Create a new project
        """
        db = 'eu11'
        storage = ['s3-rsobucketfr']
        ws_server = settings.KAIRNIAL_WS_SERVER
        front_server = settings.KAIRNIAL_FRONT_SERVER
        return self.call(
            action='addProject',
            parameters=[name, db, storage, ws_server, front_server, None, None, True, {"centralBase": 0}])


