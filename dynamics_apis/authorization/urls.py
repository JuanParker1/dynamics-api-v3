from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import ACLViewSet, ModuleViewSet

router = DefaultRouter()
router.register(r'rights', ACLViewSet, basename='rights')
router.register(r'modules', ModuleViewSet, basename='modules')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
