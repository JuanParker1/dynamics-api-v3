"""
REST API views for Kairnial contacts
"""
import os

from django.utils.translation import ugettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from dynamics_apis.common.serializers import ErrorSerializer
from dynamics_apis.users.models.contacts import Contact
from dynamics_apis.users.serializers.users import ProjectMemberSerializer
from dynamics_apis.users.serializers.contacts import ContactQuerySerializer, ContactSerializer
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

