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
    pagination_parameters, PaginatedViewSet
from .models import Folder
from .serializers import FolderQuerySerializer, FolderSerializer, FolderDetailSerializer


class FolderViewSet(PaginatedViewSet):
    """
    A ViewSet for listing or retrieving folders.
    """

    @extend_schema(
        summary=_("List Kairnial folders"),
        description=_("List Kairnial folders on this project"),
        parameters=project_parameters + pagination_parameters + [
            OpenApiParameter(name='parent_id', type=OpenApiTypes.STR, location='query',
                             required=False, description=_("Parent folder ID")),
            FolderQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: OpenApiTypes.STR, 400: ErrorSerializer},
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
        parent_id = request.GET.get('parent_id')
        try:
            total, folder_list, page_offset, page_limit = Folder.paginated_list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                parent_id=parent_id,
                page_offset=page_offset,
                page_limit=page_limit
            )

            serializer = FolderSerializer(folder_list, many=True)
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
        summary=_("Retrieve Kairnial folder"),
        description=_("Retrieve Kairnial folder by ID"),
        parameters=project_parameters + [
            OpenApiParameter(name='id', type=OpenApiTypes.INT, location='path',
                             required=False, description=_("Folder numeric ID")),
        ],
        responses={200: OpenApiTypes.STR, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        methods=["GET"]
    )
    def retrieve(self, request: HttpRequest, client_id: str, project_id: str, pk: int):
        """
        Retrieve folder detail
        :param request: HttpRequest
        :param client_id: client ID token
        :param project_id: RGOC ID of the project
        :param pk: Numeric ID of the folder
        """
        folder = Folder.get(
            client_id=client_id,
            token=request.token,
            project_id=project_id,
            id=pk
        )
        if folder:
            serializer = FolderDetailSerializer(folder)
            return Response(data=serializer.data, content_type='application/json', status=status.HTTP_200_OK)
        else:
            return Response(_("Folder not found"), status=status.HTTP_404_NOT_FOUND)
