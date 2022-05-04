"""
REST API views for Kairnial ACL
"""

from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from dynamics_apis.common.serializers import ErrorSerializer
from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import project_parameters
from .models import ACL, Module
from .serializers import ACLSerializer, ACLQuerySerializer, ModuleSerializer


class ACLViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving groups.
    """

    @extend_schema(
        summary=_("List Kairnial authorizations"),
        description=_("List Kairnial platform new access rights"),
        parameters=project_parameters + [ACLQuerySerializer],
        responses={200: ACLSerializer, 400: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request, client_id, project_id):
        """
        Retrieve a list of authorizations
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        """
        qs = ACLQuerySerializer(data=request.GET)
        filters = {}
        if qs.is_valid():
            filters = qs.validated_data
        try:
            acl_list = ACL.list(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id,
                **filters
            )
            serializer = ACLSerializer(acl_list, many=True)
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
        summary=_("List groups with authorization"),
        description=_("List Kairnial groups associated with an access right"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("UUID of the authorization")),
            ACLQuerySerializer
        ],
        responses={200: ACLSerializer, 400: ErrorSerializer},
        methods=["GET"]
    )
    @action(methods=["GET"], detail=True, url_path="groups", url_name='acl_groups')
    def list_groups(self, request, client_id: str, project_id: str, pk: str):
        """
        List groups associated with an ACL
        :param request:
        :param client_id: ID of the client
        :param project_id: RGOC ID of the project
        :param pk: ACL UUID
        :return:
        """
        pass


class ModuleViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving groups.
    """

    @extend_schema(
        summary=_("List Kairnial modules"),
        description=_("List Kairnial application modules"),
        parameters=project_parameters,
        responses={200: ModuleSerializer, 400: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request, client_id, project_id):
        """
        Retrieve a list of authorizations
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        """
        try:
            module_list = Module.list(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id
            )
            serializer = ModuleSerializer(module_list, many=True)
            return Response(serializer.data, content_type="application/json")
        except (KairnialWSServiceError, KeyError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
