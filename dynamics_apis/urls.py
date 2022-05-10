"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView, SpectacularRedocView

from .authentication import urls as authenticate_urls
from .authorization import urls as authorization_urls
from .controls import urls as controls_urls
from .defects import urls as defects_urls
from .documents import urls as document_urls
from .graphql import urls as graphql_urls
from .projects import urls as project_urls
from .users import urls as users_urls

project_path = '<str:client_id>/<str:project_id>/'

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('<str:client_id>/authentication/', include(authenticate_urls)),
    path('<str:client_id>/projects/', include(project_urls)),
    path(project_path + 'dms/', include(document_urls)),
    path(project_path + 'controls/', include(controls_urls)),
    path(project_path + 'defects/', include(defects_urls)),
    path(project_path + 'admin/', include(users_urls)),
    path(project_path + 'admin/', include(authorization_urls)),
    path('graphql', include(graphql_urls)),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
