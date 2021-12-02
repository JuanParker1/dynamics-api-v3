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
from dynamics_apis.users.models import User
from dynamics_apis.users.serializers import UserSerializer, UserCreationSerializer, UserQuerySerializer, \
    ProjectMemberSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError


class UserViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving users.
    """

    @extend_schema(
        description="List Kairnial users",
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token")),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc")),
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
        responses={200: UserSerializer, 500: ErrorSerializer},
        methods=["GET"]
    )
    def retrieve(self, request, pk):
        """
        Retrieve a Kairnial user by ID
        :param request:
        :param pk: ID of the user
        :return: KUser
        """
        try:
            user = User.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, content_type="application/json")
        except User.DoesNotExist:
            return Response(_("Invalid user"), status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Create a Kairnial user",
        parameters=[
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
