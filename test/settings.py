"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import string
import random
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

def generate_secret(nb: int = 128):
    return ''.join([random.choice(string.printable) for i in range(nb)])

SECRET_KEY = generate_secret()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'django_filters',
    'drf_spectacular',
    'oauth2_provider',
    'ariadne_django',
    'dynamics_apis.common',
    'dynamics_apis.authentication',
    'dynamics_apis.users',
    'dynamics_apis.authorization',
    'dynamics_apis.projects',
    'dynamics_apis.documents',
    'dynamics_apis.graphql',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'dynamics_apis.common.middlewares.KairnialAuthMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'test.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'test.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dynamics_apis.authentication.authentication.KairnialTokenAuthentication',
    ),

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'services': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'authentication': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Kairnial API',
    'DESCRIPTION': """
<h1>Kairnial API version 2</h1>

<p>This API is a REST frontend to the Kairnial Web Services.</p>
<p>To use this API, you must obtain a client ID, a user API key and an API secret from our customer support.</p>


<h2>1. Obtain a authentication header</h2>
To use this API, you must first <a href="#/authentication/authentication_key_create">obtain a token</a> using the authentication endpoint for this platform.


One this token obtain, pass the token in the request header using the Authenticate header.
e.g.: Authenticate: Bearer <Token>

<h2>2. Select a project</h2>
Use <a href="#/projects/projects_list">project list</a> to select a project.

""",
    'VERSION': '1.99.0',
    # OTHER SETTINGS
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authentication"
            },
        }
    },
    "SECURITY": [{"ApiKeyAuth": [], 'clientID': []}],
}

from dynamics_apis.settings import *

# KAIRNIAL_AUTH_PUBLIC_KEY = load_key(path=os.path.join(os.path.dirname(__file__), os.environ.get(
#     'KAIRNIAL_AUTH_PUBLIC_KEY_PATH', '')))
#
KAIRNIAL_AUTH_PUBLIC_KEY = os.environ.get('KAIRNIAL_AUTH_PUBLIC_KEY')

KIARNIAL_AUTH_DOMAIN = os.environ.get('KAIRNIAL_AUTH_DOMAIN', '')
# Kairnial auth server public key for token validation
KAIRNIAL_AUTH_SERVER = 'https://' + KIARNIAL_AUTH_DOMAIN
KAIRNIAL_CROSS_SERVER = os.environ.get('KAIRNIAL_CROSS_SERVER', '')
KAIRNIAL_WS_SERVER = os.environ.get('KAIRNIAL_WS_SERVER', '')
KAIRNIAL_FRONT_SERVER = os.environ.get('KAIRNIAL_FRONT_SERVER', '')
