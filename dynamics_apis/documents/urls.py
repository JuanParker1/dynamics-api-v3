"""
URLs for Kairnial Files module
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from  .viewsets import FolderViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'folders', FolderViewSet, basename='folders')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
