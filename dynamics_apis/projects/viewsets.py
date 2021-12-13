"""
Views for Kairnial projects
"""
import os
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import Project
from .serializers import ProjectSerializer, ProjectCreationSerializer, ProjectUpdateSerializer
from dynamics_apis.common.serializers import ErrorSerializer
from .services import KairnialProject
from dynamics_apis.common.services import KairnialWSServiceError


class ProjectViewSet(ViewSet):
    """
    Obtain the list of projects for a connected user
    """

    @extend_schema(
        description="Get a list of projects",
        request=ProjectSerializer,
        parameters=[
            OpenApiParameter("search", OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description=_("Search project name containing")),
        ],
        responses={200: ProjectSerializer, 400: KairnialWSServiceError},
        methods=["GET"]
    )
    def list(self, request, client_id, format=None):

        try:
            project_list = Project.list(
                client_id=client_id,
                token=request.token,
                search=request.GET.get('search')
            )
            serializer = ProjectSerializer(project_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KairnialWSServiceError as e:
            error = ErrorSerializer({
                'status': 400,
                'error': e.status,
                'description': e.message
            })
            return Response(error.data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Create a Kairnial project",
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
        ],
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
        description="Update a Kairnial project",
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
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