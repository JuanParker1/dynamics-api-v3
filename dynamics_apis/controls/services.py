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
        parameters = {
            'LIMITSKIP': offset,
            'LIMITTAKE': limit
        }
        if filters:
            parameters.update({key: value for key, value in filters.items() if value})
        return self.call(action='getTemplates', parameters=[parameters])

    def get(self, template_uuid: str):
        """
        Get an instance of a control template
        :param template_uuid: UUID of the control template
        """
        parameters = [{'template_uuid': template_uuid}]
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
        parameters = {
            'LIMITSKIP': offset,
            'LIMITTAKE': limit
        }
        if filters:
            parameters.update({key: value for key, value in filters.items() if value})
        return self.call(action='getInstances', parameters=[parameters])

    def get(self, instance_uuid: str):
        """
        Get an instance of a control
        """
        parameters = [{'instance_uuid': instance_uuid}]
        return self.call(action='getInstances', parameters=parameters)

class KairnialFormControlInstanceService(KairnialWSService):
    """
    Control Instances service using formControls
    """
    service_domain = 'formControls'

    def list(self, template_id: str, filters: dict = None, offset: int = 0,
             limit: int = getattr(settings, 'PAGE_SIZE', 100)):
        """
        List control instances
        :param filters: Serialized ControlInstanceQuerySerializer
        :param offset: value of first element in a list
        :param limit: number of elements to fetch
        :param template_id: UUID of the template
        :return:
        """
        parameters = {
            'limitSkip': offset,
            'limitTake': limit,
            'templateArray': [template_id, ]
        }
        if filters:
            parameters.update({key: value for key, value in filters.items() if value})
        parameters += [{}]
        resp = self.call(action='getMultipleInstances', service='formControls', parameters=[parameters])
        if 'error' in resp:
            return {'items': []}
        return resp