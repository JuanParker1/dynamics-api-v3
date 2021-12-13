"""
REST API views for Kairnial ACL
"""
import os
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


from dynamics_apis.common.serializers import ErrorSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError

from .models import ACL
from .serializers import ACLSerializer, ACLQuerySerializer


class ACLViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving groups.
    """

    @extend_schema(
        description="List Kairnial authorizations",
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')),
            ACLQuerySerializer
        ],
        responses={200: ACLSerializer, 500: ErrorSerializer},
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