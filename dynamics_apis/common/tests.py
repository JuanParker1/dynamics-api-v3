"""
Common test cases
"""
import datetime
import os

from django.test import TestCase
# Create your tests here.
from dotenv import load_dotenv
from rest_framework import serializers
from rest_framework.test import APIClient

from dynamics_apis.authentication.serializers import AuthResponseSerializer

load_dotenv()

from dynamics_apis.authentication.services import KairnialAuthentication

TEST_API_KEY = os.environ.get('DEFAULT_KAIRNIAL_API_KEY', '')
TEST_API_SECRET = os.environ.get('DEFAULT_KAIRNIAL_API_SECRET', '')
TEST_CLIENT_ID = os.environ.get('DEFAULT_KAIRNIAL_CLIENT_ID', '')
TEST_PROJECT_ID = os.environ.get('DEFAULT_KAIRNIAL_PROJECT_ID', '')


class KairnialClient(APIClient):
    client_id = None
    project_id = None

    def __init__(self, access_token: str, client_id: str, project_id: str,
                 enforce_csrf_checks: bool = False, **defaults):
        self.client_id = client_id
        self.project_id = project_id
        super().__init__(enforce_csrf_checks=enforce_csrf_checks, **defaults)
        self.credentials(HTTP_AUTHENTICATION='Bearer ' + access_token)

    def get(self, path, data=None, follow=False, **extra):
        path = f'/{self.client_id}/{self.project_id}/{path}'
        return super().get(path, data=data, follow=follow, **extra)

    def post(self, path, data=None, format=None, content_type=None,
             follow=False, **extra):
        path = f'/{self.client_id}/{self.project_id}/{path}'
        return super().post(path, data=data, format=format, content_type=content_type,
                            follow=follow, **extra)

    def put(self, path, data=None, format=None, content_type=None,
            follow=False, **extra):
        path = f'/{self.client_id}/{self.project_id}/{path}'
        return super().put(path, data=data, format=format, content_type=content_type, follow=follow,
                           **extra)

    def patch(self, path, data=None, format=None, content_type=None,
              follow=False, **extra):
        path = f'/{self.client_id}/{self.project_id}/{path}'
        return super().patch(path, data=data, format=format, content_type=content_type,
                             follow=follow,
                             **extra)

    def delete(self, path, data=None, format=None, content_type=None,
               follow=False, **extra):
        path = f'/{self.client_id}/{self.project_id}/{path}'
        return super().delete(path, data=data, format=format, content_type=content_type,
                              follow=follow,
                              **extra)

    def options(self, path, data=None, format=None, content_type=None,
                follow=False, **extra):
        path = f'/{self.client_id}/{self.project_id}/{path}'
        return super().options(path, data=data, format=format, content_type=content_type,
                               follow=follow,
                               **extra)


class CommonTest(TestCase):
    client_id = None
    project_id = None
    access_token = None

    def setUp(self) -> None:
        self.assertIsNotNone(self.access_token)

    @classmethod
    def setUpTestData(cls):
        cls.client_id = TEST_CLIENT_ID
        cls.project_id = TEST_PROJECT_ID
        cls.access_token = cls.get_token()

    @classmethod
    def get_token(cls):
        ka = KairnialAuthentication(client_id=cls.client_id)
        auth_response = ka.secrets_authentication(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            scopes="direct-login project-list"
        )
        access_token = AuthResponseSerializer(auth_response).data.get('access_token')
        return access_token


class HypothesisInput:
    field_type = None
    min = None
    max = None
    validators = None
    allow_null = False
    allow_blank = False

def to_hypothesis_attributes(self):
    """
    Convert Serializer field to hypothesis attributes
    Allows automatic testing via hypothesis
    1. convert Field to its python
    2. get min max values and other field attributes
    """
    t = type(self)
    try:
        func = str(t).lower().replace('field', '_handler')
        return func(self)
    except AttributeError as e:
        print(e)
        return None

def charfield_handler(self, hi: HypothesisInput):
    hi = HypothesisInput()
    hi.field_type = str
    hi.min = self.min_length
    hi.max = self.max_length
    return hi

def integerfield_handler(self, hi: HypothesisInput):
    hi = HypothesisInput()
    hi.field_type = int
    hi.min = self.min_value
    hi.max = self.max_value
    return hi

def booleanfield_handler(self, hi: HypothesisInput):
    hi = HypothesisInput()
    hi.field_type = bool
    return hi

def datefield_handler(self, hi: HypothesisInput):
    hi = HypothesisInput()
    hi.field_type = datetime.date
    return hi

def datetimefield_handler(self, hi: HypothesisInput):
    hi = HypothesisInput()
    hi.field_type = datetime.datetime
    return hi

def emailfield_handler(self, hi: HypothesisInput):
    hi = HypothesisInput()
    hi.field_type = str
    return hi

def uuidfield_handler(self, hi: HypothesisInput):
    hi = HypothesisInput()
    hi.field_type = str
    return hi

def listefield_handler(self, hi:HypothesisInput):
    return self.child.to_hypothesis_attributes()