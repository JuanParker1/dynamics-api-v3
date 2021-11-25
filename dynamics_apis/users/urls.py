from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  .viewsets import KUserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', KUserViewSet, basename='users')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]