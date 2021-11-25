"""
Kairnial authentication middleware
"""

from django.conf import settings
from django.http import JsonResponse
from jose import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

KAIRNIAL_AUTH_DOMAIN = settings.KIARNIAL_AUTH_DOMAIN
API_AUDIENCE = settings.KAIRNIAL_AUDIENCE
ALGORITHMS = ["RS256"]

KAIRNIAL_AUTH_PUBLIC_KEY = settings.KAIRNIAL_AUTH_PUBLIC_KEY

class KairnialAuthMiddleware(object):
    """
    Check the jwt token passed by the request
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def jwt_get_username_from_payload_handler(payload):
        username = payload.get('sub').replace('|', '.')
        authenticate(remote_user=username)
        return username

    def __call__(self, request):
        # GET TOKEN
        auth = request.META.get('HTTP_AUTHENTICATION')

        if not auth:
            # No auth information, skipping
            response = self.get_response(request)
            return response


        parts = auth.split()

        if parts[0].lower() != "bearer":
            return JsonResponse(data={"code": "invalid_header",
                                      "description":
                                          "Authorization header must start with"
                                          "Bearer"}, status=401)
        elif len(parts) == 1:
            return JsonResponse(data={"code": "invalid_header",
                                      "description": "Token not found"}, status=401)
        elif len(parts) > 2:
            return JsonResponse(data={"code": "invalid_header",
                                      "description": "Authorization header must be"
                                                     "Bearer token"}, status=401)

        token = parts[1]

        # VALIDATE TOKEN

        jwks = KAIRNIAL_AUTH_PUBLIC_KEY
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:

            return JsonResponse(data={"code": "invalid_header",
                                      "description": "Invalid header. "
                                                     "Use an RS256 signed JWT Access Token"}, status=401)

        if unverified_header["alg"] == "HS256":
            return JsonResponse(data={"code": "invalid_header",
                                      "description": "Invalid header. "
                                                     "Use an RS256 signed JWT Access Token"}, status=401)

        try:
            payload = jwt.decode(
                token,
                KAIRNIAL_AUTH_PUBLIC_KEY,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                #issuer="https://" + KAIRNIAL_AUTH_DOMAIN + "/"
            )
            uuid = payload.get('sub')
            first_name, last_name = payload.get('name').split()
            email = payload.get('email').split()
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.uuid=uuid
            request.user = user

        except jwt.ExpiredSignatureError:
            return JsonResponse(data={"code": "token_expired",
                                      "description": "token is expired"}, status=401)
        except jwt.JWTClaimsError as e:
            print("Invalid claim", e)
            return JsonResponse(data={"code": "invalid_claims",
                                      "description": "incorrect claims,"
                                                     " please check the audience and issuer"}, status=401)
        except Exception as e:
            print(e)
            return JsonResponse(data={"code": "invalid_header",
                                      "description": "Unable to parse authentication"
                                                     " token."}, status=400)

        response = self.get_response(request)
        return response
