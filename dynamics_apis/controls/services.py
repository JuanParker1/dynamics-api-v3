"""
Services that get and push information to Kairnial WS servers
"""

from django.conf import settings

from dynamics_apis.common.services import KairnialWSService


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

    def get(self, template_uuid: str):
        """
        Get an instance of a control template
        :param template_uuid: UUID of the control template
        """
        parameters = [{'template_uuid': template_uuid}]
        return self.call(action='getTemplates', parameters=parameters)

    def attachments(self, template_id: str):
        """
        Get file attachments on template by ID
        :param template_id: Numerric ID of the template
        """
        # TODO: test function arguments and returned values
        parameters = {'templateId': template_id}
        return self.call(action='getAttachedFilesByTemplateId', service='formControls', parameters=parameters)


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
        parameters = []
        if filters:
            parameters = [{key: value} for key, value in filters.items()]
        parameters += [
            {'limitSkip': offset},
            {'limitTake': limit}
        ]
        parameters += [{'templateArray': [template_id, ]}]
        resp = self.call(action='getMultipleInstances', service='formControls', parameters=parameters)
        if 'error' in resp:
            return {'items': []}
        return resp
