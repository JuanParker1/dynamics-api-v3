"""
Services that get and push information to Kairnial WS servers
"""
import json
import time
import uuid

import requests
from django.conf import settings

from dynamics_apis.common.services import KairnialWSService, KairnialWSServiceError

REQUESTS_METHODS = {
    'put': requests.put,
    'post': requests.post,
    'get': requests.get
}


class KairnialControlTemplateService(KairnialWSService):
    """
    Service that fetches and pushes folders
    """
    service_domain = 'controls'

    def list(self, parent_id: str = None, filters: dict = None):
        """
        List folders
        :param parent_id: ID of the parent folder, optional
        :return:
        """
        parameters = []
        if filters:
            parameters = [{key: value} for key, value in filters.items()]
        if parent_id:
            parameters.append({'asyncFolderId': parent_id})
        return self.call(action='getFlexDossiers', parameters=parameters)