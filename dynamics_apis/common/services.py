import json
import uuid
from json import JSONDecodeError

import requests
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings

from dynamics_apis.authentication.services import KairnialAuthentication


class KairnialWSServiceError(Exception):
    message = _('Error fetching data from Kairnial WebServices')
    status = 0

    def __init__(self, message, status):
        self.status = status
        self.message = message


class KairnialWSService:
    service_domain = ''
    client_id = None
    token = None
    token_type = None
    project = None

    def __init__(self, client_id: str, token: str, project: str):
        """
        Initialize the project fecthing library
        :param token: Access token to pass to header
        """
        self.client_id = client_id
        self.token = token
        self.project = project

    @classmethod
    def from_authenticator(cls, authenticator: KairnialAuthentication, project: str):
        """
        Initiate a KairnialProject from KairnialAuthentication
        :param authenticator: KairnialAuthentication
        :return:
        """
        return cls(
            client_id=authenticator.client_id,
            token=authenticator.token,
            project=project

        )

    def get_url(self, action):
        return f'{settings.KAIRNIAL_WS_SERVER}/gateway.php'

    def get_body(self, action: str):
        return json.dumps({
            'headers': self._body_headers(),
            'params': self._parameters(),
            'service': self._service(action=action)
        })

    def get_headers(self) -> dict:
        """
        Return authentication headers for WebService
        """
        return {
            'Content-type': 'application/json',
        }

    def _body_headers(self) -> dict:
        """
        Return body headers for the WS call
        :return:
        """
        return {
            'BearerToken': self.token,
            'UserLanguage': 'fr'
        }

    def _parameters(self) -> []:
        """
        Return body parameters for the WS call
        :return:
        """
        return [{}]

    def _service(self, action: str) -> str:
        """
        Return service body
        :return:
        """
        return f'{self.project}.{self.service_domain}.{action}'

    def call(self, action: str) -> dict:
        """
        Call the Webservice with parameters
        :param action: Name of the action to perform on a domain (user.getUsers)
        """
        print(self.get_url(action=action))
        print(self.get_headers())
        print(self.get_body(action=action))
        response = requests.post(
            self.get_url(action=action),
            headers=self.get_headers(),
            data=self.get_body(action=action)
        )
        if response.status_code != 200:
            raise KairnialWSServiceError(
                message=response.content,
                status=response.status_code
            )
        else:
            try:
                return response.json()
            except JSONDecodeError as e:
                raise KairnialWSServiceError(
                    message=_("Invalid response from Web Services"),
                    status=response.status_code
                )