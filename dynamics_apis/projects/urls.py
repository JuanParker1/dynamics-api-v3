from django.urls import path

from .views import ProjectView

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', ProjectView.as_view()),
]
