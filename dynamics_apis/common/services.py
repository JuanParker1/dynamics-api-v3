import uuid

from django.contrib.auth.models import User
from django.conf import settings


class KairnialWSService:
    service_domain = ''

    def __init__(self, client_id: str, token: str, user: User, project: str):
        """
        Initialize the project fecthing library
        :param token: Access token to pass to header
        """
        self.client_id = client_id
        self.token = token
        self.user = user
        self.project = project

    def get_url(self):
        return f'{settings.KAIRNIAL_WS_SERVER}/user/{self.user.uuid}/{self.service_domain}'

    def get_body(self):
        return {
            'headers': self.headers(),
            'params': self.parameters(),
            'service': self.service()
        }

    def headers(self) -> dict:
        """
        Return body headers for the WS call
        :return:
        """
        return {
            'AppType': 'api',
            'machineid': uuid.uuid4(),
            'RVersion': '8.1',
            'SystemVersion': 'rsoHTMLv8',
            'UserLanguage': 'fr'
        }

    def parameters(self) -> dict:
        """
        Return body parameters for the WS call
        :return:
        """
        return dict()


    def service(self) -> str:
        """
        Return service body
        :return:
        """
        return self.project

    def