import json
import uuid

from hypothesis import given
from hypothesis.strategies import text, booleans, integers, emails, lists

from dynamics_apis.common.tests import CommonTest, KairnialUserClient, KairnialGroupClient
from .serializers.groups import GroupSerializer
from .serializers.users import UserUUIDSerializer, UserInviteResponseSerializer, UserQuerySerializer
from ..common.viewsets import JSON_CONTENT_TYPE


class UserTest(CommonTest):
    """
    Test user routes
    """
    list_service_class = KairnialUserClient
    list_query_serializer = UserQuerySerializer
    list_response_serializer = UserUUIDSerializer

    def setUp(self) -> None:
        self.email_uuid = str(uuid.uuid4())

    def test_100_user_list(self):
        """
        Test standard user list route
        """
        kc = KairnialUserClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.list()
        serializer = UserUUIDSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    def _test_user_list_filter(self, expected_status_code: int = 200, **filter):
        """
        common function to test different filters
        The test does not focus on the content of the response but checks that
        the server returns a 200 and that the response is serializable
        """
        kc = KairnialUserClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.list(data=filter)
        if resp.status_code != expected_status_code:
            print(resp.content)
        self.assertEqual(resp.status_code, expected_status_code)
        serializer = UserUUIDSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    @given(booleans())
    def test_102_user_list_filter_archived(self, b):
        """
        Test unarchived user
        """
        self._test_user_list_filter(archived=b)

    @given(emails())
    def test_104_user_list_filter_email(self, email):
        """
        Test user email filter
        """
        self._test_user_list_filter(email=email)

    @given(text())
    def test_108_user_list_filter_full_name(self, full_name):
        """
        Test user full_name filter
        """
        self._test_user_list_filter(full_name=full_name)

    @given(lists(integers()))
    def test_110_user_list_filter_groups(self, groups):
        """
        Test filter on user groups
        """
        # This test expects a 200 since invalid filters are removed by the serializer
        self._test_user_list_filter(
            groups=','.join(map(str, groups))
        )

    @given(lists(integers(min_value=0)))
    def test_111_user_list_filter_groups_list(self, groups):
        """
        Test filter on user groups as list of groups
        """
        self._test_user_list_filter(groups=groups)

    @given(email=emails(), first_name=text(), last_name=text(), language=lists(['en', 'fr', '', 'pt']))
    def test_113_user_create(self, email, first_name, last_name, language):
        """
        Test inviting a user
        """
        kc = KairnialUserClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.post(
            data=json.dumps({
                "users": [
                    {
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "language": language
                    }]
            }),
            content_type=JSON_CONTENT_TYPE)
        print(resp.json())
        serializer = UserInviteResponseSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.validated_data), 1)
        self.created_user_id = serializer.validated_data[0].get('user').get('id')

    def test_112_user_get(self):
        """
        Test get user with ID
        """
        kc = KairnialUserClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.retrieve(pk=0)
        serializer = UserUUIDSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    def test_114_user_delete(self):
        kc = KairnialUserClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.delete(pk=self.created_user_id)
        self.assertEqual(resp.status_code, 204)


class GroupTest(CommonTest):

    def setUp(self):
        super().setUp()
        self.group_name = str(uuid.uuid4())

    def test_100_group_list(self):
        """
        Test standard group list route
        """
        kc = KairnialGroupClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.list()
        serializer = GroupSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    @given(text())
    def test_101_group_list_filter_name(self, name):
        """
        Test standard group list route filtered by name
        """
        kc = KairnialGroupClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.list(data={'name': name})
        serializer = GroupSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    def test_112_group_get(self):
        """
        Test get user with ID
        """
        kc = KairnialGroupClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.get(pk='48f944d3-bcb2-11e7-b7a1-fa163e5e5b59')
        serializer = GroupSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    @given(name=text(), description=text())
    def test_113_group_create(self, name, description):
        """
        Test inviting a user
        """
        kc = KairnialGroupClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.post(
            data=json.dumps({
                "name": name,
                "description": description
            }),
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(resp.status_code, 201)
