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
from .models import KUser
from .serializers import KUserSerializer, KUserCreationSerializer, KUserQuerySerializer


# Create your views here.
class KUserViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving users.
    """

    @extend_schema(
        description="List Kairnial users",
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                              description=_("Client ID token")),
            KUserQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: KUserSerializer, 500: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request):

        user_list = KUser.list()
        serializer = KUserSerializer(user_list, many=True)
        return Response(serializer.data, content_type="application/json")

    @extend_schema(
        description="Retrieve a Kairnial user",
        responses={200: KUserSerializer, 500: ErrorSerializer},
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
            user = KUser.get(pk=pk)
            serializer = KUserSerializer(user)
            return Response(serializer.data, content_type="application/json")
        except KUser.DoesNotExist:
            return Response(_("Invalid user"), status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Create a Kairnial user",
        parameters=[
            KUserCreationSerializer,  # serializer fields are converted to parameters
        ],
        responses={201: KUserSerializer, 500: ErrorSerializer, 400: ErrorSerializer},
        methods=["POST"]
    )
    def create(self, request):
        """
        Create a Kairnial user. Requires user creation rights
        :param request:
        :return:
        """
        pass
