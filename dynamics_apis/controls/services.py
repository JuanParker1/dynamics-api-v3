"""
Services that get and push information to Kairnial WS servers
"""

import requests
from django.conf import settings

from dynamics_apis.common.services import KairnialWSService

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

    def list(self, filters: dict = None, offset: int = 0,
             limit: int = getattr(settings, 'PAGE_SIZE', 100)):
        """
        List folders
        :param filters: Serialized ControlTemplateQuerySerializer
        :param offset: value of first element in a list
        :param limit: number of elements to fetch
        :return:
        """
        parameters = []
        if filters:
            parameters = [{key: value} for key, value in filters.items()]
        parameters += [
            {'LIMITSKIP': offset},
            {'LIMITTAKE': limit}
        ]
        return self.call(action='getTemplates', parameters=parameters)


class KairnialControlInstanceService(KairnialWSService):
    """
    Service that fetches and pushes folders
    """
    service_domain = 'controls'

    def list(self, filters: dict = None, offset: int = 0,
             limit: int = getattr(settings, 'PAGE_SIZE', 100)):
        """
        List folders
        :param filters: Serialized ControlInstanceQuerySerializer
        :param offset: value of first element in a list
        :param limit: number of elements to fetch
        :return:
        """
        parameters = []
        if filters:
            parameters = [{key: value} for key, value in filters.items()]
        parameters += [
            {'LIMITSKIP': offset},
            {'LIMITTAKE': limit}
        ]
        return self.call(action='getInstances', parameters=parameters)
