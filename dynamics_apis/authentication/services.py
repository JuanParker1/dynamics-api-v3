"""
Kairnial auth services
"""
from base64 import b64encode

import requests
import json
from django.utils.translation import ugettext as _
from django.conf import settings

PASSWORD_LOGIN_PATH = '/api/oauth2/login'
API_AUTHENT_PATH = '/api/oauth2/client_credentials/{clientID}'


class KairnialAuthenticationError(Exception):
    message = _("Invalid authentication information")


class KairnialAuthentication:
    """
    Kairnial aauthentication class
    """

    def password_authentication(self, client_id: str, username: str, password: str) -> dict:
        """
        Get atuh token from auth server
        :param client_id: Client ID, ask Kairnial support for one
        :param username: User unique identifier
        :param password: User password
        :return:
        """
        payload = {
            'client_id': client_id,
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
                _(f"Authentication failed with code {response.status_code}: {response.content}"))

        return response.json()

    def secrets_authentication(self, client_id: str, api_key: str, api_secret: str) -> dict:
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
            settings.KAIRNIAL_AUTH_SERVER + API_AUTHENT_PATH.format(clientID=client_id),
            headers=headers,
            data=payload
        )
        if response.status_code != 200:
            raise KairnialAuthenticationError(
                _(f"Authentication failed with code {response.status_code}: {response.content}"))

        return response.json()
