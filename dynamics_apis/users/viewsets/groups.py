"""
REST API views for Kairnial users
"""
import os
from django.utils.translation import ugettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from dynamics_apis.common.serializers import ErrorSerializer
from dynamics_apis.users.models.groups import Group
from dynamics_apis.users.serializers.groups import GroupSerializer, GroupQuerySerializer, GroupCreationSerializer, \
    GroupAddUserSerializer
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
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')),
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
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')),

        ],
        responses={200: GroupSerializer, 500: ErrorSerializer},
        methods=["GET"]
    )
    def retrieve(self, request, client_id: str, project_id: str, pk: str):
        """
        Retrieve a Kairnial group by ID

        :return: KU
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        :param pk: ID of the groupser
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
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')),
        ],
        request=GroupCreationSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    def create(self, request,  client_id: str, project_id: str):
        """
        Create a Kairnial user. Requires user creation rights
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        """
        gcs = GroupCreationSerializer(data=request.data)
        if gcs.is_valid():
            group = gcs.create(gcs.validated_data)
            created = group.create(
                client_id=client_id,
                token=request.token,
                project_id=project_id
            )
            if created:
                return Response(_("Group created"), status=status.HTTP_201_CREATED)
            else:
                return Response(_("Group could not be created"), status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(gcs.errors, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Add users to a group",
        parameters= [
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')),
        ],
        request=GroupAddUserSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    @action(['POST'], detail=True, url_path='users/add', url_name="add_users_to_group")
    def add_users(self, request,  client_id: str, project_id: str, pk):
        """
        Add a list of users to a group
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        :param pk: ID of the group
        """
        try:
            print("users", request.data)
            user_list = map(int, request.data.get('users'))
            resp = Group.add_users(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                pk=pk,
                user_list=user_list)
            if not resp:
                error = ErrorSerializer({
                    'status': 400,
                    'code': 0,
                    'description': _("Not all users could be added to group")
                })
                return Response(error.data, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
            return Response(_("Users added to group"), status=status.HTTP_201_CREATED)
        except ValueError as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': _("Invalid user IDs")
            })
            return Response(error.data, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Remove users from a group",
        parameters= [
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')),
        ],
        request=GroupAddUserSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    @action(['POST'], detail=True, url_path='users/remove', url_name="remove_users_from_group")
    def remove_users(self, request,  client_id: str, project_id: str, pk):
        """
        Remove a list of users to a group
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        :param pk: ID of the group
        """
        try:
            user_list = map(int, request.data.get('users'))
            resp = Group.remove_users(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                pk=pk,
                user_list=user_list)
            if not resp:
                error = ErrorSerializer({
                    'status': 400,
                    'code': 0,
                    'description': _("Not all users could be removed from group")
                })
                return Response(error.data, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
            return Response(_("Users removed from group"), status=status.HTTP_201_CREATED)
        except ValueError as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': _("Invalid user IDs")
            })
            return Response(error.data, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)