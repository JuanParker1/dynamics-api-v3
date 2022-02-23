"""
Control viewsets
"""

from django.http import HttpRequest
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from dynamics_apis.common.serializers import ErrorSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import project_parameters, PaginatedResponse, \
    pagination_parameters, PaginatedViewSet
from .models import ControlTemplate, ControlInstance
from .serializers import ControlQuerySerializer, ControlTemplateSerializer, ControlInstanceSerializer


class ControlTemplateViewSet(PaginatedViewSet):
    """
    A ViewSet for listing or retrieving documents.
    """
    parser_classes = (MultiPartParser,)

    @extend_schema(
        summary=_("List Kairnial templates"),
        description=_("List Kairnial control templates on this project"),
        parameters=project_parameters + pagination_parameters + [
            ControlQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: ControlTemplateSerializer, 400: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request: HttpRequest, client_id: str, project_id: str):
        """
        List documents on a projects
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        cqs = ControlQuerySerializer(data=request.GET)
        cqs.is_valid()
        page_offset, page_limit = self.get_pagination(request=request)
        try:
            total, template_list, page_offset, page_limit = ControlTemplate.paginated_list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                page_offset=page_offset,
                page_limit=page_limit,
                filters=cqs.validated_data
            )

            serializer = ControlTemplateSerializer(template_list, many=True)
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


class ControlInstanceViewSet(PaginatedViewSet):
    """
    A ViewSet for listing or retrieving documents.
    """
    parser_classes = (MultiPartParser,)

    @extend_schema(
        summary=_("List Kairnial instances"),
        description=_("List Kairnial control instances on this project"),
        parameters=project_parameters + pagination_parameters + [
            ControlQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: ControlInstanceSerializer, 400: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request: HttpRequest, client_id: str, project_id: str):
        """
        List documents on a projects
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        cqs = ControlQuerySerializer(data=request.GET)
        cqs.is_valid()
        page_offset, page_limit = self.get_pagination(request=request)
        try:
            total, instance_list, page_offset, page_limit = ControlInstance.paginated_list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                page_offset=page_offset,
                page_limit=page_limit,
                filters=cqs.validated_data
            )

            serializer = ControlInstanceSerializer(instance_list, many=True)
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