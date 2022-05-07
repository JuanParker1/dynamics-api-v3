"""
REST API views for Kairnial users
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
from dynamics_apis.users.models.users import User, UserNotFound
from dynamics_apis.users.serializers.users import UserSerializer, UserCreationSerializer, UserQuerySerializer, \
    ProjectMemberSerializer, ProjectMemberCountSerializer, UserGroupSerializer, UserInviteSerializer, \
    UserInviteResponseSerializer, UserMultiInviteSerializer, UserMultiInviteResponseSerializer, UserUUIDSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError


class UserViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving users.
    """

    @extend_schema(
        summary=_("List Kairnial users"),
        description=_("List Kairnial users on this project"),
        parameters=project_parameters + [
            UserQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: UserUUIDSerializer, 500: ErrorSerializer},
        tags=['admin/users', ],
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
        serializer = UserQuerySerializer(data=request.GET)
        serializer.is_valid()
        try:
            user_list = User.list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                filters=serializer.validated_data
            )
            serializer = UserUUIDSerializer(user_list, many=True)
            return Response(serializer.data, content_type="application/json")
        except (KairnialWSServiceError, KeyError, AttributeError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Count Kairnial users"),
        description=_("Count the number of active users on the project"),
        parameters=project_parameters,
        responses={200: ProjectMemberCountSerializer, 500: ErrorSerializer},
        tags=['admin/users', ],
        methods=["GET"]
    )
    @action(["GET"], detail=False, description=_("Count users for this project"), url_path='count', name="count_users")
    def count(self, request, client_id, project_id):
        """
        Count users on a project
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        try:
            user_count = User.count(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id
            )
            serializer = ProjectMemberCountSerializer(user_count)
            return Response(serializer.data, content_type="application/json")
        except (KairnialWSServiceError, KeyError, AttributeError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Retrieve a Kairnial user"),
        description=_("Get information on a specific project user"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("User Unique ID")),
        ],
        responses={200: UserUUIDSerializer, 400: ErrorSerializer},
        tags=['admin/users', ],
        methods=["GET"]
    )
    def retrieve(self, request, client_id: str, project_id: str, pk: str):
        """
        Retrieve a Kairnial user by ID
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :param pk: UUID of the user
        :return: KUser
        """
        try:
            user = User.get(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id,
                pk=pk
            )
            serializer = UserUUIDSerializer(user)
            return Response(serializer.data, content_type="application/json")
        except UserNotFound:
            return Response(_("User not found"), status=status.HTTP_404_NOT_FOUND)


    @extend_schema(
        summary=_("Retrieve current Kairnial user"),
        description=_("Get information on the current connected user"),
        parameters=project_parameters,
        responses={200: ProjectMemberSerializer, 400: ErrorSerializer},
        tags=['admin/users', ],
        methods=["GET"]
    )
    @action(['GET'], detail=False, url_path='me', url_name="me")
    def me(self, request, client_id: str, project_id: str):
        """
        Get info for connected user
        """
        try:
            user_list = User.list(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id
            )
            for user in user_list:
                if user.get('account_email') == request.user.email:
                    serializer = ProjectMemberSerializer(user)
                    return Response(serializer.data, content_type="application/json")
            error = ErrorSerializer({
                'status': 404,
                'code': 0,
                'description': _("User not found")
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_404_NOT_FOUND)
        except (KairnialWSServiceError, KeyError, AttributeError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary=_("List Kairnial user groups"),
        description=_("List groups for Kairnial user"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH,
                             description=_("User Numeric ID")),
        ],
        responses={200: UserGroupSerializer, 400: ErrorSerializer},
        tags=['admin/users', ],
        methods=["GET"]
    )
    @action(["GET"], detail=True, description=_("List groups for this user"), url_path='groups', name="groups")
    def groups(self, request, client_id: str, project_id: str, pk: int):
        """
        List groups on a project
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :param pk: User Numeric ID
        :return:
        """
        try:
            user_groups = User.groups(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id,
                pk=pk
            )
            serializer = UserGroupSerializer({'group_ids': user_groups})
            return Response(serializer.data, content_type="application/json")
        except (KairnialWSServiceError, KeyError, AttributeError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Imvite new users"),
        description=_("Invite new users into project"),
        request=UserMultiInviteSerializer,
        parameters=project_parameters,
        responses={200: [UserInviteResponseSerializer], 400: ErrorSerializer},
        tags=['admin/users', ],
        methods=["POST"]
    )
    def create(self, request, client_id, project_id):
        """

        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        user_list = UserMultiInviteSerializer(data=request.data)
        if not user_list.is_valid():
            return Response(user_list.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            invites = User.invite(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id,
                users=user_list.validated_data.get('users')
            )
            serializer = UserInviteResponseSerializer(invites, many=True)
            return Response(serializer.data, content_type="application/json")
        except (KairnialWSServiceError, KeyError, AttributeError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Archive user"),
        description=_("Archive user on project"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("User Unique ID")),
        ],
        responses={204: OpenApiTypes.STR, 400: ErrorSerializer},
        tags=['admin/users', ],
        methods=["DELETE"]
    )
    def destroy(self, request, client_id: str, project_id: str, pk: str):
        """

        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :param pk: User UUID
        :return:
        """
        archived = User.archive(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            pk=pk
        )
        return Response(_("User archived"), status=status.HTTP_204_NO_CONTENT)