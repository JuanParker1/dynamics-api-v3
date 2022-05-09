"""
Kairnial controls module models
"""

from dynamics_apis.common.models import PaginatedModel
from dynamics_apis.controls.services import KairnialControlTemplateService, KairnialControlInstanceService, \
    KairnialFormControlInstanceService


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
            filters: dict = None,
            user_id: str = None
    ):
        """
        List control templates
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param filters: serialized values from a ControlTemplateQuerySerializer
        :param user_id: Optional User ID
        :return:
        """
        kf = KairnialControlTemplateService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
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
            template_id: str,
            user_id: str = None
    ):
        """
        List ccontents from a control template
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param template_id: UUID of the template to fetch
        :param user_id: Optional User ID
        :return:
        """
        kf = KairnialControlTemplateService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        if template:=kf.list(filters={'template_uuid': template_id}):
            try:
                return template.get('items')[0].get('content')
            except IndexError:
                return None
        return None


class ControlTemplateAttachment(PaginatedModel):
    """
    Class for control templates file attachments
    """

    @staticmethod
    def list(
            client_id: str,
            token: str,
            project_id: str,
            template_id: str
    ):
        """
        List file attachments for a template
        """
        kf = KairnialControlTemplateService(client_id=client_id, token=token, project_id=project_id)
        return kf.attachments(template_id=template_id)


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
            filters: dict = None,
            template_id: str = None,
            user_id: str = None
    ):
        """
        List control instances for a template
        :param client_id: ID of the client
        :param token: Access token
        :param project_id: RGOC Code of the project
        :param template_id: UUID of the template
        :param user_id: Optional User ID
        :return:
        """

        if template_id:
            kf = KairnialFormControlInstanceService(
                client_id=client_id,
                token=token,
                user_id=user_id,
                project_id=project_id
            )
            instances = kf.list(template_id=template_id, filters=filters, limit=page_limit, offset=page_offset)
        else:
            kf = KairnialControlInstanceService(
                client_id=client_id,
                token=token,
                user_id=user_id,
                project_id=project_id
            )
            instances = kf.list(
                filters=filters, limit=page_limit, offset=page_offset
            )
        for i, instance in enumerate(instances.get('items')):
            if type(instance.get('content')) == list:
                content = [
                    {
                        'position': i,
                        'value': element.get('value', ''),
                        'date': element.get('date', '')
                    }
                    for i, element in enumerate(instance.get('content'))
                ]
                instances['items'][i]['values'] = content
            elif type(instance.get('content')) == dict:
                instances['items'][i]['values'] = [
                    {
                        'position': key,
                        'date': value.get('date'),
                        'value': value.get('value', '')
                    } for key, value in instance.get('content', {}).items() if
                    key != 'additionalInfos' and key != 'settings'
                ]
                instances['items'][i]['additional_info'] = instances['items'][i]['content'].get('additionalInfos')
        return instances
