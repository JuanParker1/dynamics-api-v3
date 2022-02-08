"""
Viewsets for the Kairnial approvals module
"""
from django.http import HttpRequest
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response

from dynamics_apis.common.serializers import ErrorSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import project_parameters, PaginatedResponse, \
    pagination_parameters, PaginatedViewSet
from ..models import ApprovalType
from ..serializers.approvals import ApprovalTypeSerializer


class ApprovalTypeViewSet(PaginatedViewSet):
    """
    A ViewSet for listing approval types
    """

    @extend_schema(
        summary=_("List Kairnial types of approvals"),
        description=_("List Kairnial approval types on this project"),
        parameters=project_parameters + pagination_parameters,
        responses={200: ApprovalTypeSerializer, 400: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request: HttpRequest, client_id: str, project_id: str):
        """
        List users on a projects
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        page_offset, page_limit = self.get_pagination(request=request)
        try:
            total, approval_type_list, page_offset, page_limit = ApprovalType.paginated_list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                page_offset=page_offset,
                page_limit=page_limit
            )

            serializer = ApprovalTypeSerializer(approval_type_list, many=True)
            return PaginatedResponse(
                data=serializer.data,
                total=total,
                page_offset=page_offset,
                page_limit=page_limit
            )
        except (KairnialWSServiceError, KeyError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
