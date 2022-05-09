import functools

from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response

from dynamics_apis.common.serializers import ErrorSerializer
from dynamics_apis.common.services import KairnialWSServiceError


def handle_ws_error(f):
    """
      Handle WS errors
    """

    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        """

        """
        try:
            return f(request, *args, **kwargs)
        except (KairnialWSServiceError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    return wrapper
