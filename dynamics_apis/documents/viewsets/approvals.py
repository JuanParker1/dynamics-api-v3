"""
Viewsets for the Kairnial approvals module
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
from ..models import ApprovalType, Approval
from ..serializers.approvals import ApprovalTypeSerializer, ApprovalSerializer, \
    ApprovalUpdateSerializer
from ..serializers.documents import DocumentFilterSerializer


class ApprovalTypeViewSet(PaginatedViewSet):
    """
    A ViewSet for listing approval types
    """

    @extend_schema(
        summary=_("List Kairnial types of approvals"),
        description=_("List Kairnial approval types on this project"),
        parameters=project_parameters + pagination_parameters,
        responses={200: ApprovalTypeSerializer, 400: ErrorSerializer},
        tags=['dms/approval types', ],
        methods=["GET"]
    )
    def list(self, request: HttpRequest, client_id: str, project_id: str):
        """
        List approval types on a projects
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :return:
        """
        page_offset, page_limit = self.get_pagination(request=request)
        try:
            total, approval_type_list, page_offset, page_limit = ApprovalType.paginated_list(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id,
                page_offset=page_offset,
                page_limit=page_limit
            )

            serializer = ApprovalTypeSerializer(approval_type_list, many=True)
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
        summary=_("Archive Kairnial approval type"),
        description=_("Archive Kairnial approval type by ID"),
        parameters=project_parameters + [
            OpenApiParameter(name='id', type=OpenApiTypes.INT, location='path',
                             required=False, description=_("Approval type numeric ID")),
        ],
        responses={204: OpenApiTypes.STR, 400: ErrorSerializer, 404: OpenApiTypes.STR},
        tags=['dms/approval types', ],
        methods=["DELETE"]
    )
    def destroy(self, request: HttpRequest, client_id: str, project_id: str, pk: int):
        """
        Archive document
        :param request: HTTPRequest
        :param client_id: ID of the client
        :param project_id: Project RGOC
        :param pk: Numeric ID of the document
        """
        archived = ApprovalType.archive(
            client_id=client_id,
            token=request.token,
            user_id=request.user_id,
            project_id=project_id,
            id=pk
        )
        if archived:
            return Response(_("Approval type archived"), status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(_("Approval type could not be archived"),
                            status=status.HTTP_406_NOT_ACCEPTABLE)



class ApprovalViewSet(PaginatedViewSet):
    """
    Viewset for approvals
    """

    @extend_schema(
        summary=_("List Kairnial approvals for folder"),
        description=_("List Kairnial approvals on a folder"),
        parameters=project_parameters + pagination_parameters + [
            DocumentFilterSerializer
        ],
        responses={200: ApprovalSerializer, 400: ErrorSerializer},
        tags=['dms/approvals', ],
        methods=["GET"]
    )
    def list(self, request: HttpRequest, client_id: str, project_id: str):
        """
        List approvals on a project
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :param folder_id: ID of the folder
        :return:
        """
        page_offset, page_limit = self.get_pagination(request=request)
        try:
            total, approval_list, page_offset, page_limit = Approval.paginated_list(
                client_id=client_id,
                token=request.token,
                user_id=request.user_id,
                project_id=project_id,
                page_offset=page_offset,
                page_limit=page_limit
            )

            print(approval_list[0].keys())

            serializer = ApprovalSerializer(approval_list, many=True)
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
        summary=_("Retrieve approval - NOT IMPLEMENTED"),
        exclude=True,
        description=_("Retrieve approval by ID"),
        parameters=project_parameters + pagination_parameters + [
            ApprovalUpdateSerializer,
        ],
        responses={200: OpenApiTypes.INT, 400: ErrorSerializer},
        tags=['dms/approvals', ],
        methods=["GET"],

    )
    def retrieve(self, request: HttpRequest, client_id: str, project_id: str, pk: int):
        """
        Get approval detail by ID
        :param request:
        :param client_id: Client ID token
        :param project_id: Project RGOC ID
        :param folder_id: ID of the folder
        :return:
        """
        # TODO: Get only one approval
        return Response("Not implemented", status=status.HTTP_501_NOT_IMPLEMENTED)

    @extend_schema(
        summary=_("List Kairnial approvals for folder"),
        description=_("List Kairnial approvals on a folder"),
        parameters=project_parameters + pagination_parameters + [
            ApprovalUpdateSerializer,
        ],
        responses={200: OpenApiTypes.INT, 400: ErrorSerializer},
        tags=['dms/approvals', ],
        methods=["PUT"]
    )
    def update(self, request: HttpRequest, client_id: str, project_id: str, pk: int):
        """
        Approval update view
        """
        aus = ApprovalUpdateSerializer(data=request.data)
        if not aus.is_valid():
            return Response(aus.errors, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        approval_id, step_id, ok = Approval.update(
            client_id=client_id,
            project_id=project_id,
            token=request.token,
            user_id=request.user_id,
            document_id=aus.validated_data.get('document_id'),
            workflow_id=aus.validated_data.get('workflow_id'),
            approval_id=pk,
            new_status=aus.validated_data.get('new_status'),
        )
        if ok:
            return Response(step_id, content_type='text/text', status=status.HTTP_200_OK)
