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

client_parameters = [
    OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                     description=_("Client ID obtain from Kairnial support"),
                     examples=[default_client_example]),
]

project_parameters = client_parameters + [
    OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                     description=_("ID of the project, usually starts with rgoc"),
                     examples=[default_project_example]),
]
