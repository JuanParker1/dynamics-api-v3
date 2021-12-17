"""
Call to Kairnial Web Services
"""
import json
import logging
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
    service_domain = 'release'
    client_id = None
    token = None
    token_type = 'Bearer'
    logger = logging.getLogger('services')

    def list(self, search: str = None) -> []:
        """
        List projects
        :return:
        """
        logger = logging.getLogger('services')
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
        logger.debug(url)
        logger.debug(headers)
        logger.debug(data)
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

    def create(self, serialized_project):
        """
        Create a new project
        :param serialized_project: ProjectCreationSerializer validated_data
        """
        return self.call(
            action='adminEC.registerProject',
            parameters=[serialized_project],
            use_cache=False
        )

    def update(self, pk, serialized_update_project):
        """
        Update un existing project
        :param serialized_update_project: ProjectUpdateSerializer validated_date
        :return:
        """
        serialized_update_project['g_nom'] = pk
        return self.call(
            action='adminEC.updateProjectInfos',
            parameters=[serialized_update_project],
            use_cache=False
        )

