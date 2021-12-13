from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import ACLViewSet

router = DefaultRouter()
router.register(r'', ACLViewSet, basename='acls')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
