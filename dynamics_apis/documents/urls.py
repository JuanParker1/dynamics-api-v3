"""
URLs for Kairnial Files module
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets.folders import FolderViewSet
from .viewsets.documents import DocumentViewSet
from .viewsets.approvals import ApprovalTypeViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'folders', FolderViewSet, basename='folders')
router.register(r'documents', DocumentViewSet, basename='documents')
router.register(r'approvals/types', ApprovalTypeViewSet, basename='documents')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
