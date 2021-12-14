"""
Common code related to viewsets
"""
import os
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

default_client_example = OpenApiExample(
    name='Default clientID',
    value=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')
)

default_project_example = OpenApiExample(
    name='Default ProjectID',
    value=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')
)

project_parameters = [
    OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                     description=_("Client ID token"),
                     examples=[default_client_example]),
    OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                     description=_("ID of the project, usually starts with rgoc"),
                     examples=[default_project_example]),
]

client_parameters = [
    OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                     description=_("Client ID token"),
                     examples=[default_client_example]),
]
