# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.blacklist.exceptions import (
    MissingToken,
)

KAIRNIAL_AUTH_DOMAIN = settings.KIARNIAL_AUTH_DOMAIN
KAIRNIAL_AUTH_PUBLIC_KEY = settings.KAIRNIAL_AUTH_PUBLIC_KEY
API_AUDIENCE = settings.KAIRNIAL_AUDIENCE
ALGORITHMS = ["RS256"]


class KairnialTokenAuthentication(JSONWebTokenAuthentication):
    """
    Token based authentication using the JSON Web Token standard.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string specified in the setting
    `JWT_AUTH_HEADER_PREFIX`. For example:

        Authorization: Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        logger = logging.getLogger('authentication')
        try:
            token = request.META.get('HTTP_AUTHENTICATION').split()[1]
            if token is None:
                return None
        except (AttributeError, IndexError):
            return None

        try:
            print(request.client_id)
            payload = jwt.decode(
                token,
                KAIRNIAL_AUTH_PUBLIC_KEY,
                algorithms=ALGORITHMS,
                audience=request.client_id
            )
            uuid = payload.get('sub')
            first_name, last_name = payload.get('name').split()
            email = payload.get('email').split()
            user = get_user_model()(
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.uuid = uuid
            return user, token

        except jwt.ExpiredSignatureError:
            logger.error("Token expired")
            return None
        except (jwt.InvalidIssuerError, jwt.InvalidAudienceError) as e:
            logger.error("incorrect claims, please check the audience and issuer")
            return None
        except AttributeError as e:
            logger.error("Unable to get client_id")
            return None
        except Exception as e:
            logger.error("Unable to parse authentication")
            return None
