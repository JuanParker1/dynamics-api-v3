"""
Control viewsets
"""

from django.http import HttpRequest
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from dynamics_apis.common.serializers import ErrorSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import project_parameters, PaginatedResponse, \
    pagination_parameters, PaginatedViewSet
from dynamics_apis.defects.models import Defect
from dynamics_apis.defects.serializers import DefectQuerySerializer, DefectSerializer, DefectCreateSerializer


class DefectViewSet(PaginatedViewSet):
    """
    A ViewSet for listing or retrieving documents.
    """
    parser_classes = (MultiPartParser,)

    @extend_schema(
        summary=_("List Kairnial defects"),
        description=_("List Kairnial defects on this project"),
        parameters=project_parameters + pagination_parameters + [
            DefectQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: DefectSerializer, 400: ErrorSerializer},
        tags=['dms/defects', ],
        methods=["GET"]
    )
    def list(self, request: HttpRequest, client_id: str, project_id: str):
        """
        List defects on a projects
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        dqs = DefectQuerySerializer(data=request.GET)
        dqs.is_valid()
        page_offset, page_limit = self.get_pagination(request=request)
        try:
            total, defect_list, page_offset, page_limit = Defect.paginated_list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                page_offset=page_offset,
                page_limit=page_limit,
                filters=dqs.validated_data
            )
            print(defect_list)
            serializer = DefectSerializer(defect_list, many=True)
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
        summary=_("Create Kairnial folder"),
        description=_("Create Kairnial"),
        parameters=project_parameters,
        request=DefectCreateSerializer,
        responses={201: DefectSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['dms/defects', ],
        methods=["POST"]
    )
    def create(self, request: HttpRequest, client_id: str, project_id: str):
        """
        Create folder
        """
        dcs = DefectCreateSerializer(data=request.data)
        if not dcs.is_valid():
            return Response(dcs.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
        defect = Defect.create(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            serialized_data=dcs.validated_data
        )
        if defect:
            serializer = DefectSerializer(defect)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(_("Defect could not be created"),
                            status=status.HTTP_406_NOT_ACCEPTABLE)
