"""
REST API views for Kairnial ACL
"""

from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from dynamics_apis.common.serializers import ErrorSerializer

from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import project_parameters, JSON_CONTENT_TYPE
from .models import ACL, Module
from .serializers import ACLSerializer, ACLQuerySerializer, \
    ModuleSerializer, TransmitterSerializer
from ..common.decorators import handle_ws_error


class ACLViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving groups.
    """

    @extend_schema(
        summary=_("List Kairnial authorizations"),
        description=_("List Kairnial platform new access rights"),
        parameters=project_parameters + [ACLQuerySerializer],
        responses={200: ACLSerializer, 400: ErrorSerializer},
        tags=['admin/acls', ],
        methods=["GET"]
    )
    @handle_ws_error
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
        acl_list = ACL.list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            **filters
        )
        serializer = ACLSerializer(acl_list, many=True)
        return Response(serializer.data, content_type=JSON_CONTENT_TYPE)

    @extend_schema(
        summary=_("List groups with authorization"),
        description=_("List Kairnial groups associated with an access right"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("UUID of the authorization")),
            ACLQuerySerializer
        ],
        responses={200: ACLSerializer, 400: ErrorSerializer},
        tags=['admin/acls', ],
        methods=["GET"]
    )
    @action(methods=["GET"], detail=True, url_path="groups", url_name='acl_groups')
    @handle_ws_error
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

    @extend_schema(
        summary=_("List defect transmitters"),
        description=_("List Kairnial transmitters allowed for the current user"),
        parameters=project_parameters,
        responses={200: TransmitterSerializer, 400: ErrorSerializer},
        tags=['admin/acls', ],
        methods=["GET"]
    )
    @action(methods=["GET"], detail=False, url_path="transmitters", url_name='acl_transmitters')
    @handle_ws_error
    def list_transmitters(self, request, client_id: str, project_id: str):
        """
        List defect transmitters
        :param request:
        :param client_id: ID of the client
        :param project_id: RGOC ID of the project
        :return:
        """
        transmitter_list = ACL.transmitters(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id
        )
        serializer = TransmitterSerializer(transmitter_list, many=True)
        return Response(serializer.data, content_type=JSON_CONTENT_TYPE)


class ModuleViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving groups.
    """

    @extend_schema(
        summary=_("List Kairnial modules"),
        description=_("List Kairnial application modules"),
        parameters=project_parameters,
        responses={200: ModuleSerializer, 400: ErrorSerializer},
        tags=['admin/modules', ],
        methods=["GET"]
    )
    @handle_ws_error
    def list(self, request, client_id, project_id):
        """
        Retrieve a list of authorizations
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        """
        module_list = Module.list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id
        )
        serializer = ModuleSerializer(module_list, many=True)
        return Response(serializer.data, content_type=JSON_CONTENT_TYPE)
