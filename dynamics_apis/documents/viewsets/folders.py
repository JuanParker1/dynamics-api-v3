"""
Viewsets for the Kairnial files module
"""
from django.http import HttpRequest
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response

from dynamics_apis.common.serializers import ErrorSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import project_parameters, PaginatedResponse, \
    pagination_parameters, PaginatedViewSet, JSON_CONTENT_TYPE, TokenRequest
from ..models import Folder
from ..serializers.folders import FolderQuerySerializer, FolderSerializer, FolderDetailSerializer, \
    FolderUpdateSerializer, FolderCreateSerializer
from ...common.decorators import handle_ws_error


class FolderViewSet(PaginatedViewSet):
    """
    A ViewSet for listing or retrieving folders.
    """

    @extend_schema(
        summary=_("List Kairnial folders"),
        description=_("List Kairnial folders on this project"),
        parameters=project_parameters + pagination_parameters + [
            OpenApiParameter(name='parent_id', type=OpenApiTypes.STR, location='query',
                             description=_("Parent folder ID")),
            FolderQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: FolderSerializer, 400: ErrorSerializer},
        tags=['dms/folders', ],
        methods=["GET"]
    )
    @handle_ws_error
    def list(self, request: TokenRequest, client_id: str, project_id: str):
        """
        List users on a projects
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        fqs = FolderQuerySerializer(data=request.GET)
        fqs.is_valid()
        page_offset, page_limit = self.get_pagination(request=request)
        parent_id = request.GET.get('parent_id')
        total, folder_list, page_offset, page_limit = Folder.paginated_list(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            parent_id=parent_id,
            page_offset=page_offset,
            page_limit=page_limit,
            filters=fqs.validated_data
        )
        serializer = FolderSerializer(folder_list, many=True)
        return PaginatedResponse(
            data=serializer.data,
            total=total,
            page_offset=page_offset,
            page_limit=page_limit
        )

    @extend_schema(
        summary=_("Retrieve Kairnial folder"),
        description=_("Retrieve Kairnial folder by ID"),
        parameters=project_parameters + [
            OpenApiParameter(name='id', type=OpenApiTypes.INT, location='path',
                             required=True, description=_("Folder numeric ID")),
        ],
        responses={200: FolderSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['dms/folders', ],
        methods=["GET"]
    )
    @handle_ws_error
    def retrieve(self, request: TokenRequest, client_id: str, project_id: str, pk: int):
        """
        Retrieve folder detail
        :param request: TokenRequest
        :param client_id: client ID token
        :param project_id: RGOC ID of the project
        :param pk: Numeric ID of the folder
        """
        folder = Folder.get(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            id=pk
        )
        if folder:
            serializer = FolderDetailSerializer(folder)
            return Response(data=serializer.data, content_type=JSON_CONTENT_TYPE, status=status.HTTP_200_OK)
        else:
            return Response(_("Folder not found"), status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary=_("Create Kairnial folder"),
        description=_("Create Kairnial"),
        parameters=project_parameters,
        request=FolderCreateSerializer,
        responses={201: FolderSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['dms/folders', ],
        methods=["POST"]
    )
    @handle_ws_error
    def create(self, request: TokenRequest, client_id: str, project_id: str):
        """
        Create folder
        """
        fcs = FolderCreateSerializer(data=request.data)
        if not fcs.is_valid():
            return Response(fcs.errors, content_type=JSON_CONTENT_TYPE,
                            status=status.HTTP_400_BAD_REQUEST)
        folder = Folder.create(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            serialized_data=fcs.validated_data
        )
        if folder:
            serializer = FolderDetailSerializer(folder)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(_("Folder could not be created"),
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @extend_schema(
        summary=_("Update Kairnial folder"),
        description=_("Update Kairnial folder by ID"),
        parameters=project_parameters + [
            OpenApiParameter(name='id', type=OpenApiTypes.INT, location='path',
                             required=True, description=_("Folder numeric ID")),
        ],
        request=FolderUpdateSerializer,
        responses={200: OpenApiTypes.STR, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['dms/folders', ],
        methods=["PUT"]
    )
    @handle_ws_error
    def update(self, request: TokenRequest, client_id: str, project_id: str, pk: int):
        """
        Update folder name and description
        """
        fus = FolderUpdateSerializer(data=request.data)
        if not fus.is_valid():
            return Response(fus.errors, content_type=JSON_CONTENT_TYPE,
                            status=status.HTTP_400_BAD_REQUEST)
        updated = Folder.update(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            id=pk,
            serialized_data=fus.validated_data
        )
        if updated:
            return Response(_("Folder updated"), status=status.HTTP_200_OK)
        else:
            return Response(_("Folder could not be updated"),
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @extend_schema(
        summary=_("Archive Kairnial folder"),
        description=_("Archive Kairnial folder by ID"),
        parameters=project_parameters + [
            OpenApiParameter(name='id', type=OpenApiTypes.UUID, location='path',
                             required=True, description=_("Folder universal ID")),
        ],
        responses={204: OpenApiTypes.STR, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['dms/folders', ],
        methods=["DELETE"]
    )
    @handle_ws_error
    def destroy(self, request: TokenRequest, client_id: str, project_id: str, pk: str):
        """
        Archive folder
        :param request: TokenRequest
        :param client_id: ID of the client
        :param project_id: Project RGOC
        :param pk: UUID of the folder
        """
        archived = Folder.archive(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            id=pk
        )
        if archived:
            return Response(_("Folder archived"), status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(_("Folder could not be archived"),
                            status=status.HTTP_406_NOT_ACCEPTABLE)
