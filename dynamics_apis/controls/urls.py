"""
URLs for Kairnial Files module
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import ControlTemplateViewSet, ControlInstanceViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'templates/(?P<pk>/instances', ControlInstanceViewSet, basename='control_instances')
router.register(r'templates', ControlTemplateViewSet, basename='control_templates')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
