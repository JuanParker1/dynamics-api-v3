from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import ProjectViewSet

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='projects')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
