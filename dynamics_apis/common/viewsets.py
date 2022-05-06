"""
Common code related to viewsets
"""
import os
from django.utils.translation import gettext as _
from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

default_client_example = OpenApiExample(
    name='Default clientID',
    value=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')
)

default_project_example = OpenApiExample(
    name='Default ProjectID',
    value=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')
)

client_parameters = [
    OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                     exclude=True,
                     description=_("Client ID obtain from Kairnial support"),
                     examples=[default_client_example]),
]

project_parameters = client_parameters + [
    OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                     description=_("ID of the project, usually starts with rgoc"),
                     examples=[default_project_example]),
]

pagination_parameters = [
    OpenApiParameter("page_offset", OpenApiTypes.INT, OpenApiParameter.QUERY,
                     description=_("Offset in results for pagination"), default=0),
    OpenApiParameter("page_limit", OpenApiTypes.INT, OpenApiParameter.QUERY,
                     description=_("Number of results per page"), default=getattr(settings, 'PAGE_SIZE', 100)),
]


class PaginatedViewSet(ViewSet):

    def get_pagination(self, request):
        """
        Extract pagination from request and return page_offset, page_limit
        """
        try:
            page_limit = int(request.GET.get('page_limit'))
            page_offset = int(request.GET.get('page_offset'))
        except ValueError:
            page_offset = 0
            page_limit = getattr(settings, 'PAGE_SIZE', 100)
        return page_offset, page_limit



class PaginatedResponse:

    def __new__(
            cls,
            data,
            total,
            page_offset,
            page_limit
    ):
        output = {
            'total': total,
            'items': data,
            'page_offset': page_offset,
            'page_limit': page_limit
        }
        return Response(
            output,
            content_type='application/json',
            status=status.HTTP_200_OK
        )
