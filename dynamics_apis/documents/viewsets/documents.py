"""
Document viewsets
"""

from django.http import HttpRequest
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from dynamics_apis.common.serializers import ErrorSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import project_parameters, PaginatedResponse, \
    pagination_parameters, PaginatedViewSet
from ..models import Document, Folder
from ..serializers.documents import DocumentQuerySerializer, DocumentSerializer, \
    DocumentCreateSerializer, DocumentReviseSerializer, DocumentSearchRevisionSerializer, \
    DocumentSearchRevisionSupplementaryArguments, DocumentRevisionSerializer, \
    DocumentSearchPathSerializer, DocumentRevisionTreeSerializer
from ...common.decorators import handle_ws_error


class DocumentViewSet(PaginatedViewSet, ):
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
        tags=['dms/documents', ],
        methods=["GET"]
    )
    @handle_ws_error
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
        total, document_list, page_offset, page_limit = Document.paginated_list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
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

    @extend_schema(
        summary=_("Retrieve Kairnial document"),
        description=_("Retrieve Kairnial document by ID"),
        parameters=project_parameters + [
            OpenApiParameter(name='id', type=OpenApiTypes.INT, location='path',
                             required=False, description=_("Folder numeric ID")),
        ],
        responses={200: DocumentSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['dms/documents', ],
        methods=["GET"]
    )
    @handle_ws_error
    def retrieve(self, request: HttpRequest, client_id: str, project_id: str, pk: int):
        """
        Retrieve folder detail
        :param request: HttpRequest
        :param client_id: client ID token
        :param project_id: RGOC ID of the project
        :param pk: Numeric ID of the document
        """
        document = Document.get(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            id=pk
        )
        if document:
            serializer = DocumentSerializer(document)
            return Response(data=serializer.data, content_type='application/json', status=status.HTTP_200_OK)
        else:
            return Response(_("Document not found"), status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary=_("Check if a document exists "),
        description=_("Returns existing document and revisions"),
        parameters=project_parameters + [
            DocumentSearchPathSerializer,
            DocumentSearchRevisionSerializer,
            DocumentSearchRevisionSupplementaryArguments
        ],
        responses={200: DocumentRevisionTreeSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        methods=["GET"],
        tags=['dms/documents',]
    )
    @action(methods=['GET'], detail=False, url_path='check_revisions', url_name='check_revisions')
    @handle_ws_error
    def check_revisions(self, request, client_id, project_id, *args, **kwargs):
        """
        Create a new document
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        data = request.GET.copy()
        dps = DocumentSearchPathSerializer(data=data)
        drs = DocumentSearchRevisionSerializer(data=data)
        dss = DocumentSearchRevisionSupplementaryArguments(data=data)
        if not dps.is_valid() or not drs.is_valid() or not dss.is_valid():
            errors = {}
            try:
                errors.update(dps.errors)
                errors.update(drs.errors)
                errors.update(dss.errors)
            except AssertionError:
                pass
            return Response(errors, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        folder_list = Folder.list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            filters={
                'exact_path': dps.validated_data.get('path'),
            }
        )
        revisions = []
        for folder in folder_list:
            dss.validated_data['folderRestricionId'] = folder.get('fcat_id')
            revision = Document.check_revision(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id,
                document_serialized_data=drs.validated_data,
                supplementary_serialized_data=dss.validated_data
            )
            if revision:
                revisions.append(revision)
        if not revisions:
            return Response(_("File not found"), status=status.HTTP_404_NOT_FOUND)
        drs = DocumentRevisionTreeSerializer(revisions, many=True)
        return Response(drs.data, content_type="application/json")

    @extend_schema(
        summary=_("Create Kairnial document with file"),
        description=_("Create Kairnial document"),
        parameters=project_parameters,
        request=DocumentCreateSerializer,
        responses={201: DocumentSerializer,
                   400: ErrorSerializer,
                   404: OpenApiTypes.STR,
                   417: OpenApiTypes.STR},
        tags=['dms/documents', ],
        methods=["POST"]
    )
    @handle_ws_error
    def create(self, request: HttpRequest, client_id: str, project_id: str):
        """
        Create a new document
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        data = request.POST.copy()
        data.update(request.FILES)
        dcs = DocumentCreateSerializer(data=data)
        if not dcs.is_valid():
            return Response(dcs.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            document = Document.create(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id,
                serialized_data=dcs.validated_data,
                attachment=request.FILES.get('file')
            )
            if not document:
                return Response("Could not fetch resulting document",
                                status=status.HTTP_417_EXPECTATION_FAILED)
            serializer = DocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KairnialWSServiceError as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Revise Kairnial document"),
        description=_("Revise Kairnial document"),
        parameters=project_parameters,
        request=DocumentReviseSerializer,
        responses={201: DocumentSerializer,
                   400: ErrorSerializer,
                   404: OpenApiTypes.STR,
                   417: OpenApiTypes.STR},
        tags=['dms/documents', ],
        methods=["PUT"]
    )
    @handle_ws_error
    def update(self, request: HttpRequest, client_id: str, project_id: str, pk: str):
        """
        Update document information
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :param pk: UUID of the document
        :return:
        """
        data = request.POST.copy()
        data.update(request.FILES)
        dcs = DocumentCreateSerializer(data=data)
        if not dcs.is_valid():
            return Response(dcs.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
        document = Document.update(
            parent_id=pk,
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            serialized_data=dcs.validated_data,
            attachment=request.FILES.get('file')
        )
        if not document:
            return Response("Could not fetch resulting document",
                            status=status.HTTP_417_EXPECTATION_FAILED)
        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary=_("Archive Kairnial document"),
        description=_("Archive Kairnial document by ID"),
        parameters=project_parameters + [
            OpenApiParameter(name='id', type=OpenApiTypes.INT, location='path',
                             required=False, description=_("Document numeric ID")),
        ],
        responses={204: OpenApiTypes.STR, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['dms/documents', ],
        methods=["DELETE"]
    )
    @handle_ws_error
    def destroy(self, request: HttpRequest, client_id: str, project_id: str, pk: int):
        """
        Archive document
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: Project RGOC
        :param pk: Numeric ID of the document
        """
        archived = Document.archive(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            id=pk
        )
        if archived:
            return Response(_("Document archived"), status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(_("Document could not be archived"),
                            status=status.HTTP_406_NOT_ACCEPTABLE)
