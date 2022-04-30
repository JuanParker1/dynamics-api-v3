from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets.contacts import ContactViewSet
from .viewsets.groups import GroupViewSet
from .viewsets.users import UserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'contacts', ContactViewSet, basename='contacts')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
