"""
REST API views for Kairnial users
"""
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from dynamics_apis.common.serializers import ErrorSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import project_parameters, JSON_CONTENT_TYPE
from dynamics_apis.users.models.groups import Group
from dynamics_apis.users.serializers.groups import GroupSerializer, GroupQuerySerializer, GroupCreationSerializer, \
    GroupAddUserSerializer, RightSerializer, GroupAddAuthorizationSerializer

add_authorization_example = OpenApiExample(
    name='Example authorization',
    value={
        '2f4abb17-fbf4-4636-811c-44d30cb8f128': 'bim:pins',
        '443e4612-cc58-4d25-a635-53a2dab280a1': 'documents:hide_annotation'
    }
)


class GroupViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving groups.
    """

    @extend_schema(
        summary=_("List of Kairnial groups"),
        description=_("List Kairnial groups defined on the project"),
        parameters=project_parameters + [
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
            return Response(error.data, content_type=JSON_CONTENT_TYPE,
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Retrieve a group"),
        description=_("Retrieve a Kairnial group by UUID"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH,
                             description=_("UUID of the group")),

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
        summary=_("Create a Kairnial group"),
        description=_("Create a new Kairnial group on the project"),
        parameters=project_parameters,
        request=GroupCreationSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    def create(self, request, client_id: str, project_id: str):
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
            return Response(gcs.errors, content_type=JSON_CONTENT_TYPE, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Add users to a group"),
        description=_("Add an existing project user to the group"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH,
                             description=_("Numeric ID of the group")),
        ],
        request=GroupAddUserSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    @action(['POST'], detail=True, url_path='users/add', url_name="add_users_to_group")
    def add_users(self, request, client_id: str, project_id: str, pk):
        """
        Add a list of users to a group
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        :param pk: ID of the group
        """
        try:
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
        summary=_("Remove users from a group"),
        description=_("Remove a project user from the group"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH,
                             description=_("Numeric ID of the group")),
        ],
        request=GroupAddUserSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    @action(['POST'], detail=True, url_path='users/remove', url_name="remove_users_from_group")
    def remove_users(self, request, client_id: str, project_id: str, pk):
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

    @extend_schema(
        summary=_("List authorizations for group"),
        description=_("List legacy authorizations, new authorizations and modules for a group"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH,
                             description=_("UUID of the group")),
        ],
        responses={200: RightSerializer, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["GET"]
    )
    @action(['GET'], detail=True, url_path='authorizations', url_name="list_authorizations_for_group")
    def list_authorization(self, request, client_id: str, project_id: str, pk):
        """
        Add a list of rights to a group
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        :param pk: UUID of the group
        """
        try:
            group_authorizations_list = Group.list_authorizations(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                pk=pk
            )
            serializer = RightSerializer(group_authorizations_list)
            return Response(serializer.data, content_type="application/json")
        except (KairnialWSServiceError, KeyError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type=JSON_CONTENT_TYPE,
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Add authorization to a group"),
        description=_("Add a new authorizations to a group"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH,
                             description=_("UUID of the group")),
        ],
        request=GroupAddAuthorizationSerializer,
        examples=[add_authorization_example, ],
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    @action(['POST'], detail=True, url_path='authorization/add', url_name="add_authorization_to_group")
    def add_authorization(self, request, client_id: str, project_id: str, pk):
        """
        Add a list of rights to a group
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        :param pk: UUID of the group
        """
        try:
            resp = Group.add_authorizations(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                pk=pk,
                authorizations=request.data)
            if not resp:
                error = ErrorSerializer({
                    'status': 400,
                    'code': 0,
                    'description': _("Not all authorizations could be added to group")
                })
                return Response(error.data, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
            return Response(_("Rights added to group"), status=status.HTTP_201_CREATED)
        except ValueError as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': _("Invalid authorization IDs")
            })
            return Response(error.data, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Remove authorization from a group"),
        description=_("Remove a new access right from a group"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH,
                             description=_("UUID of the group")),
        ],
        examples=[add_authorization_example, ],
        request=GroupAddAuthorizationSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    @action(['POST'], detail=True, url_path='authorization/remove', url_name="remove_authorization_from_group")
    def remove_authorization(self, request, client_id: str, project_id: str, pk):
        """
        Remove a list of users to a group
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        :param pk: UUID of the group
        """
        try:
            resp = Group.remove_authorzations(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                pk=pk,
                authorizations=request.data)
            if not resp:
                error = ErrorSerializer({
                    'status': 400,
                    'code': 0,
                    'description': _("Not all authorizations could be removed from group")
                })
                return Response(error.data, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
            return Response(_("Authorizations removed from group"), status=status.HTTP_201_CREATED)
        except ValueError as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': _("Invalid authorization IDs")
            })
            return Response(error.data, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
