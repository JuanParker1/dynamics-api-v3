import datetime
import json
import logging
from hashlib import sha1
from json import JSONDecodeError

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext as _

from dynamics_apis.common.viewsets import JSON_CONTENT_TYPE


class KairnialWSServiceError(Exception):
    message = _('Error fetching data from Kairnial WebServices')
    status = 0

    def __init__(self, message, status):
        super().__init__(message)
        self.status = status
        self.message = message


def json_with_dates(obj):
    """
    handler for json date serializer
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    else:
        return str(obj)


class KairnialService:
    service_domain = ''
    client_id = None
    token = None
    token_type = 'Bearer'

    def get_url(self):
        raise NotImplementedError

    def get_body(self, service: str, action: str, parameters: [dict] = None) -> str:
        return json.dumps({
            'headers': self._body_headers(),
            'params': parameters,
            'service': self._service(service=service, action=action)
        }, default=json_with_dates)

    def get_headers(self) -> dict:
        """
        Return authentication headers for WebService
        """
        return {
            'Content-type': JSON_CONTENT_TYPE,
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

    def _service(self, service: str, action: str) -> str:
        """
        Return service body
        :return:
        """
        return f'{service}.{action}'

    def call(
            self,
            action: str,
            service: str = '',
            parameters: [dict] = None,
            out_format: str = 'json',
            use_cache=False
        ):
        """
        Call the Webservice with parameters
        :param action: Name of the action to perform on a domain (getUsers)
        :param parameters: list of dict to send to server
        :param service: name of service (user, ...). Uses service_domain if not set
        :param format: expected output format from tre Kairnial Web Service
        :param use_cache: cache response
        """
        logger = logging.getLogger('services')
        url = self.get_url()
        headers = self.get_headers()
        data = self.get_body(
            service=service or self.service_domain,
            action=action,
            parameters=parameters or [{}]
        )
        logger.debug(f"--- call to {url} with headers {json.dumps(headers)} and data {json.dumps(data)}")
        cache_key = sha1(f'{url}||{json.dumps(headers)}||{data}'.encode('latin1')).hexdigest()
        if use_cache and (cached_data := cache.get(cache_key)):
            return cached_data
        response = requests.post(
            url=url,
            headers=headers,
            data=data
        )
        logger.debug(f"<--- response {response.status_code} with length {len(response.content)}")
        if response.status_code != 200:
            logger.debug(f"<--- error response content {response.content}")
            raise KairnialWSServiceError(
                message=response.content or 'General error',
                status=response.status_code
            )
        else:
            output = self._parse_response(response=response, out_format=out_format)
            if use_cache:
                cache.set(cache_key, output, timeout=30)
            return output

    def _parse_response(self, response, out_format: str = 'json'):
        """
        Parse response according to defined format
        :param response: HTTPResponse
        :param out_format: expected response format (int, str, json, ...)
        """
        if out_format == 'json':
            output = self._parse_json(response=response)
        elif out_format == 'int':
            output = self._parse_int(response=response)
        elif out_format == 'bool':
            output = self._parse_bool(response=response)
        else:
            output = response.content
        return output

    def _parse_json(self, response):
        """
        Convert response content to json
        """
        logger = logging.getLogger('services')
        try:
            return response.json()
        except JSONDecodeError as e:
            logger.debug(e)
            raise KairnialWSServiceError(
                message=_("Invalid response from Web Services: {}").format(),
                status=response.status_code
            ) from e

    def _parse_int(self, response):
        """
        Convert response content to int
        """
        logger = logging.getLogger('services')
        try:
            return int(response.content.decode('utf8').replace('"', ''))
        except ValueError as e:
            logger.debug(e)
            raise KairnialWSServiceError(
                message=_("Invalid response from Web Services: {}").format(str(e)),
                status=response.status_code
            ) from e

    def _parse_bool(self, response):
        """
        Convert response content to bool
        """
        logger = logging.getLogger('services')
        try:
            val = int(response.content.decode('utf8').replace('"', ''))
            return val != 0
        except ValueError as e:
            logger.debug(e)
            raise KairnialWSServiceError(
                message=_("Invalid response from Web Services: {}").format(str(e)),
                status=response.status_code
            ) from e


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
        self.client_id = client_id.strip()
        self.token = token.strip()
        self.project_id = project_id.strip()

    def get_url(self):
        return f'{settings.KAIRNIAL_WS_SERVER}/gateway.php'

    def _service(self, service: str, action: str) -> str:
        """
        Return service body
        :return:
        """
        return f'{self.project_id}.{service}.{action}'
