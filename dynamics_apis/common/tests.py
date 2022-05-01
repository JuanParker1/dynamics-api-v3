"""
Common test cases
"""
import os

from django.test import TestCase
# Create your tests here.
from dotenv import load_dotenv
from hypothesis import given
from hypothesis.strategies import text, integers, emails, uuids, lists, dates, datetimes, booleans
from rest_framework.fields import Field
from rest_framework.test import APIClient

from dynamics_apis.authentication.serializers import AuthResponseSerializer
from dynamics_apis.authentication.services import KairnialAuthentication

load_dotenv()

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


class KairnialPathClient(KairnialClient):
    path = None

    def list(self, data=None, follow=False, **extra):
        return super().get(self.path, data=data, follow=follow, **extra)

    def retrieve(self, pk, data=None, follow=False, **extra):
        return super().get(f'{self.path}/{pk}/', data=data, follow=follow, **extra)

    def post(self, data=None, format=None, content_type=None,
             follow=False, **extra):
        return super().post(self.path, data=data, format=format, content_type=content_type,
                            follow=follow, **extra)

    def put(self, pk, data=None, format=None, content_type=None,
            follow=False, **extra):
        return super().put(f'{self.path}/{pk}/', data=data, format=format, content_type=content_type,
                           follow=follow, **extra)

    def patch(self, pk, data=None, format=None, content_type=None,
              follow=False, **extra):
        return super().patch(f'{self.path}/{pk}/', data=data, format=format, content_type=content_type,
                             follow=follow, **extra)

    def delete(self, pk, data=None, format=None, content_type=None,
               follow=False, **extra):
        return super().delete(f'{self.path}/{pk}/', data=data, format=format, content_type=content_type,
                              follow=follow, **extra)

    def options(self, pk, data=None, format=None, content_type=None,
                follow=False, **extra):
        return super().options(f'{self.path}/{pk}/', data=data, format=format, content_type=content_type,
                               follow=follow, **extra)


class KairnialUserClient(KairnialPathClient):
    route = '/users'


class KairnialGroupClient(KairnialPathClient):
    route = '/groups'


class KairnialContactClient(KairnialPathClient):
    route = '/contacts'


class CommonTest(TestCase):
    client_id = None
    project_id = None
    access_token = None
    list_service_class = None
    list_query_serializer = None
    list_response_serializer = None

    def __init__(self, *args, **kwargs):
        if self.list_query_serializer:
            lqs = self.list_query_serializer()
            for name, field in lqs.fields.items():
                fhs = field.hypothesis_strategy()
                print(f"Field {name} hypothesis strategy", fhs)
                if fhs:
                    setattr(self, f'test_list_{name}', given(self.test_list, fhs))
        super().__init__(*args, **kwargs)

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
            api_secret=TEST_API_SECRET
        )
        access_token = AuthResponseSerializer(auth_response).data.get('access_token')
        return access_token

    @classmethod
    def test_list(self, expected_status_code=200):
        """
        common function to test different filters
        The test does not focus on the content of the response but checks that
        the server returns a 200 and that the response is serializable
        """
        lsc = self.list_service_class(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = lsc.list(data=filter)
        if resp.status_code != expected_status_code:
            print(resp.content)
        self.assertEqual(resp.status_code, expected_status_code)
        serializer = self.list_response_serializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())


def hypothesis_strategy(self):
    """
    Convert Serializer field to hypothesis attributes
    Allows automatic testing via hypothesis
    1. convert Field to its python
    2. get min max values and other field attributes
    """
    t = type(self)
    try:
        func = str(t).lower().replace('field', '_strategy')
        strategy = strategies[func]()
    except (AttributeError, KeyError) as e:
        print(e)
        return None


def charfield_strategy(self):
    return text(min_size=self.min_length, max_size=self.max_length)


def integerfield_strategy(self):
    return integers(min_value=self.min_value, max_value=self.max_value)


def booleanfield_strategy(self):
    return booleans()


def datefield_strategy(self):
    return dates()


def datetimefield_strategy(self):
    return datetimes()


def emailfield_strategy(self):
    return emails()


def uuidfield_strategy(self):
    return uuids()


def listfield_strategy(self):
    return lists(self.child.hypothesis_strategy())


setattr(Field, 'hypothesis_strategy', hypothesis_strategy)
setattr(Field, 'charfield_strategy', charfield_strategy)
setattr(Field, 'integerfield_strategy', integerfield_strategy)
setattr(Field, 'booleanfield_strategy', booleanfield_strategy)
setattr(Field, 'datefield_strategy', datefield_strategy)
setattr(Field, 'datetimefield_strategy', datetimefield_strategy)
setattr(Field, 'emailfield_strategy', emailfield_strategy)
setattr(Field, 'uuidfield_strategy', uuidfield_strategy)
setattr(Field, 'listfield_strategy', listfield_strategy)

strategies = {
    'charfield_strategy': charfield_strategy,
    'integerfield_strategy': integerfield_strategy,
    'booleanfield_strategy': booleanfield_strategy,
    'datefield_strategy': datefield_strategy,
    'datetimefield_strategy': datetimefield_strategy,
    'emailfield_strategy': emailfield_strategy,
    'uuidfield_strategy': uuidfield_strategy,
    'listfield_strategy': listfield_strategy
}
