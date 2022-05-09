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
    ContactCreationSerializer, ContactUpdateSerializer
# Create your views here.
from dynamics_apis.common.services import KairnialWSServiceError
from dynamics_apis.common.viewsets import project_parameters


class ContactViewSet(ViewSet):
    """
    A ViewSet for listing or retrieving contacts.
    """

    @extend_schema(
        summary=_("List Kairnial contacts"),
        description=_("List Kairnial contacts or companies on the project"),
        parameters=project_parameters + [
            ContactQuerySerializer,  # serializer fields are converted to parameters
        ],
        responses={200: ContactSerializer, 500: ErrorSerializer},
        tags=['admin/contacts', ],
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
                user_id=request.user_id,
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
        summary=_("Create a Kairnial contact"),
        description=_("Create a new contact or company on the project"),
        parameters=project_parameters,
        request=ContactCreationSerializer,
        responses={201: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        tags=['admin/contacts', ],
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
                user_id=request.user_id,
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

    @extend_schema(
        summary=_("Update a Kairnial contact"),
        description=_("Update an existing Kairnial contact or company on the project"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH,
                             description=_("UUID of the contact")),
        ],
        request=ContactUpdateSerializer,
        responses={200: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        tags=['admin/contacts', ],
        methods=["PUT"]
    )
    def update(self, request, client_id: str, project_id: str, pk: str):
        """
        Create a Kairnial user. Requires user creation rights
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: ID of the project
        :param pk: UUID of the contact
        """
        cus = ContactUpdateSerializer(data=request.data)
        if cus.is_valid():
            updated = Contact.update(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id,
                pk=pk,
                serialized_data=cus.validated_data
            )
            if updated:
                return Response(_("Contact updated"), status=status.HTTP_200_OK)
            else:
                return Response(_("Contact could not be updated"),
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(cus.errors, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary=_("Delete a Kairnial contact"),
        description=_("Delete an existing Kairnial contact or company from the project. This is a soft delete"),
        parameters=project_parameters + [
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH,
                             description=_("Numerical ID of the contact")),
        ],
        responses={204: OpenApiTypes.STR, 400: OpenApiTypes.STR, 406: OpenApiTypes.STR},
        tags=['admin/contacts', ],
        methods=["DELETE"]
    )
    def destroy(self, request, client_id: str, project_id: str, pk: int):
        """
        Archive contact
        """
        deleted = Contact.delete(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            pk=pk
        )
        if deleted:
            return Response(_("Contact deleted"), status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(_("Contact could not be deleted"),
                            status=status.HTTP_406_NOT_ACCEPTABLE)
