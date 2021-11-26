"""
Views for Kairnial projects
"""
from django.utils.translation import ugettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProjectSerializer
from dynamics_apis.common.serializers import ErrorSerializer
from .services import KairnialProject
from ..common.models import KairnialServiceError


class ProjectView(APIView):
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
        responses={200: ProjectSerializer, 400: ErrorSerializer},
        methods=["GET"]
    )
    def get(self, request, client_id, format=None):
        search = request.GET.get('search')
        kp = KairnialProject(
            client_id=client_id,
            token=request.token
        )
        try:
            response = kp.list(search=search)
            serializer = ProjectSerializer(response['items'], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KairnialServiceError as e:
            return Response(str(e), content_type='application/json', status=status.HTTP_400_BAD_REQUEST)