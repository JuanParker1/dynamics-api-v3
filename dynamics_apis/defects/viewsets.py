"""
Control viewsets
"""

from django.http import HttpRequest
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from dynamics_apis.common.decorators import handle_ws_error
from dynamics_apis.common.serializers import ErrorSerializer
# Create your views here.
from dynamics_apis.common.viewsets import project_parameters, \
    PaginatedResponse, pagination_parameters, PaginatedViewSet
from dynamics_apis.defects.models import Defect
from dynamics_apis.defects.serializers import DefectQuerySerializer, \
    DefectSerializer, DefectCreateSerializer, \
    DefectAreaSerializer, DefectBIMCategorySerializer, \
    DefectBIMLevelSerializer, DefectUpdateSerializer


class DefectViewSet(PaginatedViewSet):
    """
    A ViewSet for listing or retrieving documents.
    """

    @extend_schema(
        summary=_("List Kairnial defects"),
        description=_("List Kairnial defects on this project"),
        parameters=project_parameters + pagination_parameters + [
            DefectQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: DefectSerializer, 400: ErrorSerializer},
        tags=['defects', ],
        methods=["GET"]
    )
    @handle_ws_error
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
        total, defect_list, page_offset, page_limit = Defect.paginated_list(
            client_id=client_id,
            token=request.token,
            project_id=project_id,
            page_offset=page_offset,
            page_limit=page_limit,
            filters=dqs.validated_data,
            items_key='pins'
        )
        serializer = DefectSerializer(defect_list, many=True)
        return PaginatedResponse(
            data=serializer.data,
            total=total,
            page_offset=page_offset,
            page_limit=page_limit
        )

    @extend_schema(
        summary=_("Get Kairnial defect"),
        description=_("Get a specific defect by ID"),
        parameters=project_parameters + pagination_parameters + [
            OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH,
                             description=_("Numeric ID of the defect")),
        ],
        responses={200: DefectSerializer, 400: ErrorSerializer},
        tags=['defects', ],
        methods=["GET"]
    )
    @handle_ws_error
    def retrieve(self, request: HttpRequest, pk: str, client_id: str, project_id: str):
        """
        Get Defeect by numeric ID
        """
        defect = Defect.get(
            client_id=client_id,
            token=request.token,
            project_id=project_id,
            pk=pk
        )
        if not defect:
            return Response(_("Invalid defect"), status=status.HTTP_404_NOT_FOUND)
        serializer = DefectSerializer(defect)
        return Response(serializer.data, content_type="application/json")

    @extend_schema(
        summary=_("Create Kairnial defect"),
        description=_("Create Kairnial defect"),
        parameters=project_parameters,
        request=DefectCreateSerializer,
        exclude=True,
        responses={201: DefectSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['defects', ],
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

    @extend_schema(
        summary=_("Update defect description"),
        description=_("Update defect description"),
        parameters=project_parameters,
        request=DefectUpdateSerializer,
        responses={200: DefectSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['defects', ],
        methods=["PATCH"]
    )
    @handle_ws_error
    def patch(self, request: HttpRequest, client_id: str, project_id: str):
        """
        Patch defect
        """
        dus = DefectUpdateSerializer(data=request.data)
        if not dus.is_valid():
            return Response(dus.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("List defect areas"),
        description=_("List areas attached to defects"),
        parameters=project_parameters,
        responses={200: DefectAreaSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['defects', ],
        methods=["GET"]
    )
    @action(methods=["GET"], detail=False, url_path="areas", url_name='defect_areas')
    @handle_ws_error
    def areas(self, request: HttpRequest, client_id: str, project_id: str):
        areas = Defect.areas(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id
        )
        das = DefectAreaSerializer(areas, many=True)
        return Response(das.data, content_type='application/json')

    @extend_schema(
        summary=_("List defect BIM categories"),
        description=_("List BIM categories attached to defects"),
        parameters=project_parameters,
        responses={200: DefectBIMCategorySerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['defects', ],
        methods=["GET"]
    )
    @action(methods=["GET"], detail=False, url_path="bim_categories", url_name='defects_bim_categories')
    @handle_ws_error
    def bim_categories(self, request: HttpRequest, client_id: str, project_id: str):
        categories = Defect.bim_categories(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id
        )
        dbcs = DefectBIMCategorySerializer(categories, many=True)
        return Response(dbcs.data, content_type='application/json')

    @extend_schema(
        summary=_("List defect BIM levels"),
        description=_("List BIM levels attached to defects"),
        parameters=project_parameters,
        responses={200: DefectBIMLevelSerializer, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['defects', ],
        methods=["GET"]
    )
    @action(methods=["GET"], detail=False, url_path="bim_levels", url_name='defects_bim_levels')
    @handle_ws_error
    def bim_levels(self, request: HttpRequest, client_id: str, project_id: str):
        levels = Defect.bim_levels(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id
        )
        dbls = DefectBIMLevelSerializer(levels, many=True)
        return Response(dbls.data, content_type='application/json')
