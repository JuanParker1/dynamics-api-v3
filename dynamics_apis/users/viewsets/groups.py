"""
REST API views for Kairnial users
"""
from django.utils.translation import ugettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from dynamics_apis.common.serializers import ErrorSerializer
from dynamics_apis.users.models import Group
from dynamics_apis.users.serializers import GroupSerializer, GroupQuerySerializer, GroupCreationSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError


class GroupViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving groups.
    """

    @extend_schema(
        description="List Kairnial groups",
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token")),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc")),
            GroupQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: GroupSerializer, 500: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request, client_id, project_id):
        """
        Retrieve a list of groups
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        """
        try:
            group_list = Group.list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                filters=request.GET
            )
            serializer = GroupSerializer(group_list, many=True)
            return Response(serializer.data, content_type="application/json")
        except (KairnialWSServiceError, KeyError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Retrieve a Kairnial user",
        responses={200: GroupSerializer, 500: ErrorSerializer},
        methods=["GET"]
    )
    def retrieve(self, request, client_id, project_id, pk):
        """
        Retrieve a Kairnial group by ID
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        :param pk: ID of the group
        :return: KUser
        """
        try:
            group_list = Group.list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                filters=request.GET
            )
            group = [g for g in group_list if g.get('guid', '') == pk]
            serializer = GroupSerializer(group[0])
            return Response(serializer.data, content_type="application/json")
        except IndexError:
            return Response(_("Invalid group"), status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Create a Kairnial group",
        parameters=[
            GroupCreationSerializer,  # serializer fields are converted to parameters
        ],
        responses={201: GroupSerializer, 500: ErrorSerializer, 400: ErrorSerializer},
        methods=["POST"]
    )
    def create(self, request):
        """
        Create a Kairnial user. Requires user creation rights
        :param request:
        :return:
        """
        pass