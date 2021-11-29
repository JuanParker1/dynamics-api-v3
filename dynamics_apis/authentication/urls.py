from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  .views import PasswordAuthenticationView, APIKeyAuthenticationView

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('password', PasswordAuthenticationView.as_view()),
    path('key', APIKeyAuthenticationView.as_view()),
]