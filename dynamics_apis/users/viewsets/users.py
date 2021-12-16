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
from dynamics_apis.users.models.users import User
from dynamics_apis.users.serializers.users import UserSerializer, UserCreationSerializer, UserQuerySerializer, \
    ProjectMemberSerializer, ProjectMemberCountSerializer
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
        responses={200: ProjectMemberSerializer, 500: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request, client_id, project_id):
        try:
            user_list = User.list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                filters=request.GET
            )
            serializer = ProjectMemberSerializer(user_list, many=True)
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
        methods=["GET"]
    )
    @action(["GET"], detail=False, description=_("Count users for this project"), url_path='count', name="count_users")
    def count(self, request, client_id, project_id):
        try:
            user_count = User.count(
                client_id=client_id,
                token=request.token,
                project_id=project_id
            )
            print(user_count)
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
                             description=_("User ID")),
        ],
        responses={200: ProjectMemberSerializer, 400: ErrorSerializer},
        methods=["GET"]
    )
    def retrieve(self, request, client_id, project_id, pk):
        """
        Retrieve a Kairnial user by ID
        :param request:
        :param pk: ID of the user
        :return: KUser
        """
        try:
            user = User.get(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                pk=pk
            )[0]
            serializer = ProjectMemberSerializer(user)
            return Response(serializer.data, content_type="application/json")
        except IndexError:
            return Response(_("User not found"), status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary=_("Create a Kairnial user"),
        description=_("Create or invite a new user on the project"),
        parameters=project_parameters + [
            UserCreationSerializer,  # serializer fields are converted to parameters
        ],
        responses={201: UserSerializer, 500: ErrorSerializer, 400: ErrorSerializer},
        methods=["POST"]
    )
    def create(self, request):
        """
        Create a Kairnial user. Requires user creation rights
        :param request:
        :return:
        """
        pass

    @extend_schema(
        summary=_("Retrieve current Kairnial user"),
        description=_("Get information on the current connected user"),
        parameters=project_parameters,
        responses={200: ProjectMemberSerializer, 400: ErrorSerializer},
        methods=["GET"]
    )
    @action(['GET'], detail=False, url_path='me', url_name="me")
    def me(self, request, client_id, project_id):
        """
        Get info for connected user
        """
        try:
            user_list = User.list(
                client_id=client_id,
                token=request.token,
                project_id=project_id
            )
            for user in user_list:
                print(user.get('account_email'), request.user.email)
                if user.get('account_email') == request.user.email:
                    print(user)
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

