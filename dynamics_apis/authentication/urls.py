from django.urls import path

from .views import PasswordAuthenticationView, APIKeyAuthenticationView

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('password', PasswordAuthenticationView.as_view()),
    path('key', APIKeyAuthenticationView.as_view()),
]
