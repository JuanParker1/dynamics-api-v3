"""
Viewsets for the Kairnial files module
"""

import os

from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from dynamics_apis.common.viewsets import project_parameters
from dynamics_apis.common.serializers import ErrorSerializer
from dynamics_apis.users.models.users import User
from dynamics_apis.users.serializers.users import UserSerializer, UserCreationSerializer, UserQuerySerializer, \
    ProjectMemberSerializer, ProjectMemberCountSerializer, UserGroupSerializer, UserInviteSerializer, \
    UserInviteResponseSerializer, UserMultiInviteSerializer, UserMultiInviteResponseSerializer, UserUUIDSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError
from .serializers import FolderQuerySerializer
from .models import Folder

class FolderViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving folders.
    """

    @extend_schema(
        summary=_("List Kairnial folders"),
        description=_("List Kairnial folders on this project"),
        parameters=project_parameters + [
            OpenApiParameter(name='parent_id', type=OpenApiTypes.STR, location='query', required=False,description=_("Parent folder ID")),
            FolderQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: OpenApiTypes.STR, 500: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request, client_id, project_id):
        """
        List users on a projects
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        parent_id = request.GET.get('parent_id')
        try:
            folder_list = Folder.list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                parent_id=parent_id
            )
            print(folder_list)
            # serializer = UserUUIDSerializer(user_list, many=True)
            # return Response(serializer.data, content_type="application/json")
        except (KairnialWSServiceError, KeyError, AttributeError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
