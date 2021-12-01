import uuid
from json import JSONDecodeError

import requests
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings


class KairnialWSServiceError(Exception):
    message = _('Error fetching data from Kairnial WebServices')


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

    def get_url(self, action):
        return f'{settings.KAIRNIAL_WS_SERVER}/user/{self.user.uuid}/{self.service_domain}.{action}'

    def get_body(self):
        return {
            'headers': self._body_headers(),
            'params': self._parameters(),
            'service': self._service()
        }

    def get_headers(self) -> dict:
        """
        Return authentication headers for WebService
        """
        return {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def _body_headers(self) -> dict:
        """
        Return body headers for the WS call
        :return:
        """
        return {
            'AppType': 'api',
            'machineid': str(uuid.uuid4()),
            'RVersion': '8.1',
            'SystemVersion': 'rsoHTMLv8',
            'UserLanguage': 'fr'
        }

    def _parameters(self) -> dict:
        """
        Return body parameters for the WS call
        :return:
        """
        return dict()

    def _service(self) -> str:
        """
        Return service body
        :return:
        """
        return self.project

    def call(self, action: str) -> dict:
        """
        Call the Webservice with parameters
        """
        response = requests.post(
            self.get_url(action=action),
            headers=self.get_headers(),
            data=self.get_body()
        )
        if response.status_code != 200:
            raise KairnialWSServiceError(response.content)
        else:
            try:
                return response.json()
            except JSONDecodeError as e:
                raise KairnialWSServiceError(_("Invalid response from Web Services"))