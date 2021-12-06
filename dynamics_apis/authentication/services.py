"""
Kairnial auth services
"""
from base64 import b64encode

import requests
import json

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings

PASSWORD_LOGIN_PATH = '/api/oauth2/login'
API_AUTHENT_PATH = '/api/oauth2/client_credentials/{clientID}'


class KairnialAuthenticationError(Exception):
    message = _("Invalid authentication information")
    status = 0

    def __init__(self, message, status):
        self.status = status
        self.message = message



class KairnialAuthentication:
    """
    Kairnial aauthentication class
    """
    token_type = None
    token = None
    user = None
    client_id = None

    def __init__(self, client_id: str):
        self.client_id = client_id

    def password_authentication(self, username: str, password: str) -> dict:
        """
        Get atuh token from auth server
        :param client_id: Client ID, ask Kairnial support for one
        :param username: User unique identifier
        :param password: User password
        :return:
        """
        payload = {
            'client_id': self.client_id,
            'grant_type': 'password',
            'password': password,
            'username': username,
            'scope': 'login-token project-list'
        }
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(
            settings.KAIRNIAL_AUTH_SERVER + PASSWORD_LOGIN_PATH,
            headers=headers,
            data=payload
        )
        if response.status_code != 200:
            raise KairnialAuthenticationError(
                message=_(f"Authentication failed with code {response.status_code}: {response.content}"),
                status=response.status_code
            )

        try:
            resp = response.json()
            self._extract_token(resp)
            self._extract_token_type(resp)
            self._extract_user(resp)
            return resp
        except json.JSONDecodeError:
            raise KairnialAuthenticationError(
                message="Invalid response from server",
                status=400

            )

    def secrets_authentication(self, api_key: str, api_secret: str) -> dict:
        """
        Get auth token from auth server
        :param client_id: Client ID, ask Kairnial support for one
        :param api_key: User API Key
        :param api_secret: User API Secret
        :return:
        """
        secrets_header = b64encode(f'{api_key}:{api_secret}'.encode('latin1'))
        payload = {
            'grant_type': 'client_credentials',
             'scope': 'login-token project-list'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {secrets_header.decode("utf8")}'
        }
        response = requests.post(
            settings.KAIRNIAL_AUTH_SERVER + API_AUTHENT_PATH.format(clientID=self.client_id),
            headers=headers,
            data=payload
        )
        if response.status_code != 200:
            raise KairnialAuthenticationError(
                message=_(f"Authentication failed with code {response.status_code}: {response.content}"),
                status=response.status_code
            )


        try:
            resp = response.json()
            self._extract_token(resp)
            self._extract_token_type(resp)
            self._extract_user(resp)
            return resp
        except json.JSONDecodeError:
            raise KairnialAuthenticationError(
                message="Invalid response from server",
                status=400
            )

    def _extract_token_type(self, response: dict):
        """
        extract token from authentication response
        :param response:
        :return:
        """
        self.token_type = response.get('token_type')
        return self.token_type

    def _extract_token(self, response: dict):
        """
        extract token from authentication response
        :param response:
        :return:
        """
        self.token = response.get('access_token')
        return self.token

    def _extract_user(self, response: dict):
        """
        Extract User object from
        :param response:
        :return:
        """
        resp_user = response.get('user', {})
        user = User()
        user.first_name = resp_user.get('first_name')
        user.last_name = resp_user.get('last_name')
        user.email = resp_user.get('email')
        user.uuid = resp_user.get('uuid')
        self.user = user
        return self.user

