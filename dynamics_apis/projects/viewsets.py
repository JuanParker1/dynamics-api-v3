"""
Views for Kairnial projects
"""
import os

from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from dynamics_apis.common.serializers import ErrorSerializer
from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import client_parameters, pagination_parameters, PaginatedViewSet, PaginatedResponse
from .models import Project
from .serializers import ProjectSerializer, ProjectCreationSerializer, ProjectUpdateSerializer, \
    ProjectIntegrationSerializer


class ProjectViewSet(PaginatedViewSet):
    """
    Obtain the list of projects for a connected user
    """

    @extend_schema(
        summary=_("List projects"),
        description=_("Get a list of projects associated to current connected user"),
        request=ProjectSerializer,
        parameters=client_parameters + pagination_parameters + [
            OpenApiParameter("search", OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description=_("Search project name containing")),
        ],
        responses={200: ProjectSerializer, 400: KairnialWSServiceError},
        methods=["GET"]
    )
    def list(self, request, client_id, format=None):
        page_offset, page_limit = self.get_pagination(request=request)
        try:
            total, project_list, page_offset,page_limit = Project.paginated_list(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                search=request.GET.get('search'),
                page_offset=page_offset,
                page_limit=page_limit
            )
            serializer = ProjectSerializer(project_list, many=True)
            return PaginatedResponse(
                total=total,
                data=serializer.data,
                page_offset=page_offset,
                page_limit=page_limit
            )
        except KairnialWSServiceError as e:
            error = ErrorSerializer({
                'status': 400,
                'error': e.status,
                'description': e.message
            })
            return Response(error.data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Project discovery for Thinkproject integration"),
        description=_("Get a list of projects associated to current connected user"),
        request=ProjectSerializer,
        parameters=client_parameters + pagination_parameters + [
            OpenApiParameter("search", OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description=_("Search project name containing")),
        ],
        responses={200: ProjectIntegrationSerializer, 400: KairnialWSServiceError},
        methods=["GET"]
    )
    @action(methods=['GET', ], detail=False, url_path='discovery', url_name='discovery')
    def discover(self, request, client_id):
        """
        Integrate into CIC project
        """
        page_offset, page_limit = self.get_pagination(request=request)
        try:
            total, project_list, page_offset, page_limit = Project.integration_list(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                search=request.GET.get('search'),
                page_offset=page_offset,
                page_limit=page_limit
            )
            print(project_list)
            serializer = ProjectIntegrationSerializer(project_list, many=True)
            return PaginatedResponse(
                total=total,
                data=serializer.data,
                page_offset=page_offset,
                page_limit=page_limit
            )
        except KairnialWSServiceError as e:
            error = ErrorSerializer({
                'status': 400,
                'error': e.status,
                'description': e.message
            })
            return Response(error.data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary=_("Create a Kairnial project"),
        description=_(
            "Create a new project for the current connected user, give a template UUID to copy the configuration from an existing project"),
        parameters=client_parameters,
        request=ProjectCreationSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    def create(self, request, client_id):
        pcs = ProjectCreationSerializer(data=request.data)
        if pcs.is_valid():
            created = Project.create(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                serialized_project=pcs.validated_data
            )
            if created:
                return Response(_("Project created"), status=status.HTTP_201_CREATED)
            else:
                return Response(_("Project could not be created"),
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(pcs.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Update a Kairnial project"),
        description=_("Udpdate information on a existing project"),
        parameters=client_parameters + [
            OpenApiParameter("id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("RGOC ID of the project")),
        ],
        request=ProjectUpdateSerializer,
        responses={200: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["PUT"]
    )
    def update(self, request, client_id: str, pk: str):
        """
        View to update project
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param pk: Project RGOC
        :return: 
        """
        pus = ProjectUpdateSerializer(data=request.data)
        if pus.is_valid():
            created = Project.update(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                pk=pk,
                serialized_project=pus.validated_data
            )
            if created:
                return Response(_("Project updated"), status=status.HTTP_200_OK)
            else:
                return Response(_("Project could not be updated"),
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(pus.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
