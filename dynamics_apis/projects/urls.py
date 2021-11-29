from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  .views import ProjectView

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', ProjectView.as_view()),
]