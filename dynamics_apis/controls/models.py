"""
Kairnial controls module models
"""

from dynamics_apis.common.models import PaginatedModel
from dynamics_apis.controls.services import KairnialControlTemplateService, KairnialControlInstanceService


class ControlTemplate(PaginatedModel):
    """
    Kairnial Control template
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            page_offset: int,
            page_limit: int,
            filters: dict = None
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param filters: serialized values from a ControlTemplateQuerySerializer
        :return:
        """
        kf = KairnialControlTemplateService(client_id=client_id, token=token, project_id=project_id)
        return kf.list(filters=filters, limit=page_limit, offset=page_offset)


class ControlTemplateContent(PaginatedModel):
    """
    Kairnial Control template
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            template_id: str
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param template_id: UUID of the template to fetch
        :return:
        """
        kf = KairnialControlTemplateService(client_id=client_id, token=token, project_id=project_id)
        if template:=kf.list(filters={'template_uuid': template_id}):
            try:
                return template.get('items')[0].get('content')
            except IndexError:
                return None
        return None


class ControlInstance(PaginatedModel):
    """
    Kairnial Control instances
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            page_offset: int,
            page_limit: int,
            filters: dict = None
    ):
        """
        List children folders from a parent
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :return:
        """
        kf = KairnialControlInstanceService(client_id=client_id, token=token, project_id=project_id)
        instances = kf.list(filters=filters, limit=page_limit, offset=page_offset)
        for i, instance in enumerate(instances.get('items')):
            print(instance)
            if type(instance.get('content')) == list:
                instances['items'][i]['content']['additional_info'] = {}
                instances['items'][i]['content']['values'] = [
                    {
                        'position': i,
                        'value': element.get('value', ''),
                        'date': element.get('date', '')
                    }
                    for i, element in enumerate(instance.get('content'))
                ]
            elif type(instance.get('content')) == dict:
                instances['items'][i]['content']['additional_info'] = instance.get('additionalInfos', {})
                instances['items'][i]['content']['values'] = [
                    {
                        'position': key,
                        'date': value.get('date'),
                        'value': value.get('value', '')
                    } for key, value in instance.get('content', {}).items()
                ]
        return instances