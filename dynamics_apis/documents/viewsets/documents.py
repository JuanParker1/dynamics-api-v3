"""
Document viewsets
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
from ..models import Document
from ..serializers.documents import DocumentQuerySerializer, DocumentSerializer, \
    DocumentCreateSerializer


class DocumentViewSet(PaginatedViewSet):
    """
    A ViewSet for listing or retrieving documents.
    """
    parser_classes = (MultiPartParser,)

    @extend_schema(
        summary=_("List Kairnial documents"),
        description=_("List Kairnial documents on this project"),
        parameters=project_parameters + pagination_parameters + [
            OpenApiParameter(name='parent_id', type=OpenApiTypes.STR, location='query',
                             required=False, description=_("Parent folder ID")),
            DocumentQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: DocumentSerializer, 400: ErrorSerializer},
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
        dqs = DocumentQuerySerializer(data=request.GET)
        dqs.is_valid()
        page_offset, page_limit = self.get_pagination(request=request)
        parent_id = request.GET.get('parent_id')
        try:
            total, document_list, page_offset, page_limit = Document.paginated_list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                parent_id=parent_id,
                page_offset=page_offset,
                page_limit=page_limit,
                filters=dqs.validated_data
            )

            serializer = DocumentSerializer(document_list, many=True)
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

    @extend_schema(
        summary=_("Create Kairnial document with file"),
        description=_("Create Kairnial"),
        parameters=project_parameters,
        request=DocumentCreateSerializer,
        responses={201: DocumentSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        methods=["POST"]
    )
    def create(self, request: HttpRequest, client_id: str, project_id: str):
        """
        Create a new document
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        print(request.POST, request.FILES)
        data = request.POST.copy()
        data.update(request.FILES)
        print(data)
        dcs = DocumentCreateSerializer(data=data)
        if not dcs.is_valid():
            return Response(dcs.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            document = Document.create(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                serialized_data=dcs.validated_data,
                attachment=request.FILES.get('file')
            )
            serializer = DocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KairnialWSServiceError as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
