"""
REST API views for Kairnial contacts
"""
import os

from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from dynamics_apis.common.serializers import ErrorSerializer
from dynamics_apis.users.models.contacts import Contact
from dynamics_apis.users.serializers.users import ProjectMemberSerializer
from dynamics_apis.users.serializers.contacts import ContactQuerySerializer, ContactSerializer, \
    ContactCreationSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError


class ContactViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving contacts.
    """

    @extend_schema(
        description="List Kairnial contacts",
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')),
            ContactQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: ContactSerializer, 500: ErrorSerializer},
        methods=["GET"]
    )
    def list(self, request, client_id, project_id):
        try:
            query_serializer = ContactQuerySerializer(data=request.GET)
            if query_serializer.is_valid():
                filters = query_serializer.validated_data
            else:
                filters = {}
            contact_list = Contact.list(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                filters=filters
            )
            serializer = ContactSerializer(contact_list, many=True)
            return Response(serializer.data, content_type="application/json")
        except (KairnialWSServiceError, KeyError, AttributeError) as e:
            error = ErrorSerializer({
                'status': 400,
                'code': getattr(e, 'status', 0),
                'description': getattr(e, 'message', str(e))
            })
            return Response(error.data, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Create a Kairnial contact",
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("Client ID token"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')),
            OpenApiParameter("project_id", OpenApiTypes.STR, OpenApiParameter.PATH,
                             description=_("ID of the project, usually starts with rgoc"),
                             default=os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')),
        ],
        request=ContactCreationSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        methods=["POST"]
    )
    def create(self, request, client_id: str, project_id: str):
        """
        Create a Kairnial user. Requires user creation rights
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        """
        ccs = ContactCreationSerializer(data=request.data)
        if ccs.is_valid():
            created = Contact.create(
                client_id=client_id,
                token=request.token,
                project_id=project_id,
                serialized_data=ccs.validated_data
            )
            if created:
                return Response(_("Contact created"), status=status.HTTP_201_CREATED)
            else:
                return Response(_("Contact could not be created"),
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(ccs.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)