"""
Control viewsets
"""

from django.http import HttpRequest
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from dynamics_apis.common.serializers import ErrorSerializer
# Create your views here.
from dynamics_apis.common.viewsets import project_parameters, PaginatedResponse, \
    pagination_parameters, PaginatedViewSet
from .models import ControlTemplate, ControlInstance, ControlTemplateContent, ControlTemplateAttachment
from .serializers import ControlQuerySerializer, ControlTemplateSerializer, \
    ControlInstanceSerializer, ControlTemplateElementSerializer, ControlTemplateContentSerializer, \
    ControlTemplateAttachmentSerializer
from ..common.decorators import handle_ws_error


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
        tags=['controls/templates', ],
        methods=["GET"]
    )
    @handle_ws_error
    def list(self, request: HttpRequest, client_id: str, project_id: str):
        """
        List control templates on a projects
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        cqs = ControlQuerySerializer(data=request.GET)
        cqs.is_valid()
        page_offset, page_limit = self.get_pagination(request=request)
        total, template_list, page_offset, page_limit = ControlTemplate.paginated_list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
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

    @extend_schema(
        summary=_("List Kairnial template elements"),
        description=_("List Kairnial control template elements for one template on this project"),
        parameters=project_parameters,
        responses={200: ControlTemplateElementSerializer, 400: ErrorSerializer},
        tags=['controls/templates', ],
        methods=["GET"]
    )
    @action(methods=["GET"], detail=True, url_path="elements", url_name='template_elements')
    @handle_ws_error
    def elements(self, request: HttpRequest, client_id: str, project_id: str, pk: str):
        """
        View to list template elements
        """
        template_content = ControlTemplateContent.list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            template_id=pk
        )

        serializer = ControlTemplateContentSerializer(template_content)
        return Response(data=serializer.data, content_type='application/json')

    @extend_schema(
        summary=_("List Kairnial template attachments"),
        description=_("List Kairnial control template attachments for one template on this project"),
        parameters=project_parameters,
        responses={200: ControlTemplateElementSerializer, 400: ErrorSerializer},
        tags=['controls/templates', ],
        methods=["GET"]
    )
    @action(methods=["GET"], detail=True, url_path="attachments", url_name='template_attachments')
    @handle_ws_error
    def attachments(self, request: HttpRequest, client_id: str, project_id: str, pk: str):
        """
        View to list template attachments
        """
        template_content = ControlTemplateAttachment.list(
            client_id=client_id,
            token=request.token,
            project_id=project_id,
            template_id=pk
        )

        serializer = ControlTemplateAttachmentSerializer(template_content)
        return Response(data=serializer.data, content_type='application/json')


class ControlInstanceViewSet(PaginatedViewSet):
    """
    A ViewSet for listing or retrieving documents.
    """
    parser_classes = (MultiPartParser,)

    @extend_schema(
        summary=_("List Kairnial instances"),
        description=_("List Kairnial control instances on this project"),
        parameters=project_parameters + pagination_parameters + [
            OpenApiParameter('template_id', OpenApiTypes.STR, location='query', required=False),
            ControlQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: ControlInstanceSerializer, 400: ErrorSerializer},
        tags=['controls/instances', ],
        methods=["GET"]
    )
    @handle_ws_error
    def list(self, request: HttpRequest, client_id: str, project_id: str):
        """
        List control instances on a projects
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        cqs = ControlQuerySerializer(data=request.GET)
        cqs.is_valid()
        page_offset, page_limit = self.get_pagination(request=request)
        template_id = request.GET.get('template_id', None)
        total, instance_list, page_offset, page_limit = ControlInstance.paginated_list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            page_offset=page_offset,
            page_limit=page_limit,
            filters=cqs.validated_data,
            template_id=template_id
        )
        serializer = ControlInstanceSerializer(instance_list, many=True)
        return PaginatedResponse(
            data=serializer.data,
            total=total,
            page_offset=page_offset,
            page_limit=page_limit
        )
