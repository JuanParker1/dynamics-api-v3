import json
import logging
from hashlib import sha1
from json import JSONDecodeError

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext as _


class KairnialWSServiceError(Exception):
    message = _('Error fetching data from Kairnial WebServices')
    status = 0

    def __init__(self, message, status):
        super()
        self.status = status
        self.message = message


class KairnialService:
    service_domain = ''
    client_id = None
    token = None
    token_type = 'Bearer'

    def get_url(self):
        raise NotImplementedError

    def get_body(self, action: str, parameters: [dict] = [{}]) -> str:
        return json.dumps({
            'headers': self._body_headers(),
            'params': parameters,
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

    def _service(self, action: str) -> str:
        """
        Return service body
        :return:
        """
        return f'{self.service_domain}.{action}'

    def call(self, action: str, parameters: [dict] = [{}], format: str = 'json'):
        """
        Call the Webservice with parameters
        :param action: Name of the action to perform on a domain (user.getUsers)
        """
        logger = logging.getLogger('services')
        url = self.get_url()
        headers = self.get_headers()
        data = self.get_body(action=action, parameters=parameters)
        logger.debug(url)
        logger.debug(headers)
        logger.debug(data)
        cache_key = sha1(f'{url}||{json.dumps(headers)}||{data}'.encode('latin1')).hexdigest()
        output = cache.get(cache_key)
        if output:
            return output
        response = requests.post(
            url=url,
            headers=headers,
            data=data
        )
        logger.debug(response.status_code)
        logger.debug(response.content)
        if response.status_code != 200:
            logger.debug(response.status_code)
            logger.debug(response.content)
            raise KairnialWSServiceError(
                message=response.content or 'General error',
                status=response.status_code
            )
        else:
            if format == 'json':
                try:
                    output = response.json()
                except JSONDecodeError as e:
                    raise KairnialWSServiceError(
                        message=_("Invalid response from Web Services"),
                        status=response.status_code
                    ) from JSONDecodeError
            elif format == 'bool' or format == 'int':
                try:
                    val = int(response.content.decode('utf8').replace('"', ''))
                    if format == 'int':
                        output = val
                    else:
                        output = val != 0
                except ValueError as e:
                    logger.debug(e)
                    raise KairnialWSServiceError(
                        message=_("Invalid response from Web Services"),
                        status=response.status_code
                    ) from JSONDecodeError
            else:  # Return content as string
                output = response.content
            cache.set(cache_key, output, timeout=30)
            logger.debug(output)
            return output


class KairnialCrossService(KairnialService):

    def __init__(self, client_id: str, token: str):
        """
        Initialize the Kairnial Auth services library
        :param client_id: ID of the client
        :param token: Access token to pass to header
        :param project_id: ID of the project
        """
        self.client_id = client_id
        self.token = token

    def get_url(self):
        return f'{settings.KAIRNIAL_CROSS_SERVER}/gateway.php'


class KairnialWSService(KairnialService):
    project_id = None

    def __init__(self, client_id: str, token: str, project_id: str):
        """
        Initialize the Kairnial Web Services library
        :param client_id: ID of the client
        :param token: Access token to pass to header
        :param project_id: ID of the project
        """
        self.client_id = client_id
        self.token = token
        self.project_id = project_id

    def get_url(self):
        return f'{settings.KAIRNIAL_WS_SERVER}/gateway.php'

    def _service(self, action: str) -> str:
        """
        Return service body
        :return:
        """
        return f'{self.project_id}.{self.service_domain}.{action}'
