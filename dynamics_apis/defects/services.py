"""
Services that get and push information to Kairnial WS servers for reserves.php
"""

from django.conf import settings

from dynamics_apis.common.services import KairnialWSService


class KairnialDefectService(KairnialWSService):
    """
    Service that fetches and pushes defects
    """
    service_domain = 'reserves'



    def list(self, filters: dict = None, offset: int = 0,
             limit: int = getattr(settings, 'PAGE_SIZE', 100)):
        """
        List folders
        :param filters: Serialized DefectQuerySerializer
        :param offset: value of first element in a list
        :param limit: number of elements to fetch
        :return:
        """
        parameters = [
            {
                'limited': {
                    'lastId': offset,
                    'nbItems': limit
                }
            }
        ]
        if filters:
            parameters = [{key: value} for key, value in filters.items()]
        parameters += [offset, limit]
        return self.call(action='getFlexAllReserves', parameters=parameters)

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
