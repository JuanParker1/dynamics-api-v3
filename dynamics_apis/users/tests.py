import json
import random
import string
import uuid

from dynamics_apis.common.tests import CommonTest, KairnialClient
from .serializers.groups import GroupSerializer
from .serializers.users import UserUUIDSerializer, UserInviteResponseSerializer
from ..common.viewsets import JSON_CONTENT_TYPE


class UserTest(CommonTest):
    """
    Test user routes
    """

    def setUp(self) -> None:
        self.email_uuid = str(uuid.uuid4())

    def test_100_user_list(self):
        """
        Test standard user list route
        """
        kc = KairnialClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.get('users/')
        serializer = UserUUIDSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    def _test_user_list_filter(self, expected_status_code: int = 200, **filter):
        """
        common function to test different filters
        The test does not focus on the content of the response but checks that
        the server returns a 200 and that the response is serializable
        """
        kc = KairnialClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.get('users/', data=filter)
        if resp.status_code != expected_status_code:
            print(resp.content)
        self.assertEqual(resp.status_code, expected_status_code)
        serializer = UserUUIDSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    def test_102_user_list_filter_archived_false(self):
        """
        Test unarchived user
        """
        self._test_user_list_filter(archived=False)

    def test_103_user_list_filter_archived_true(self):
        """
        Test archived user
        """
        self._test_user_list_filter(archived=True)

    def test_104_user_list_filter_email(self):
        """
        Test user email filter
        """
        self._test_user_list_filter(email='me@test.com')

    def test_105_user_list_filter_number_email(self):
        """
        Test user email filter with a number as argument
        """
        self._test_user_list_filter(email=1)

    def test_106_user_list_filter_email_injection(self):
        """
        Test user email filter with a SQL injection pattern
        """
        self._test_user_list_filter(email="me \" OR 1")

    def test_107_user_list_filter_email_too_long(self):
        """
        Test user email filter with a very long filter
        """
        letters = string.ascii_letters + string.digits
        email = ''.join(random.choice(letters) for _ in range(10000))
        self._test_user_list_filter(email=email)

    def test_108_user_list_filter_full_name(self):
        """
        Test user full_name filter
        """
        self._test_user_list_filter(full_name="I am a full name")

    def test_109_user_list_filter_full_name_number(self):
        """
        Test user full_name filter with number as argument
        """
        self._test_user_list_filter(full_name=1)

    def test_110_user_list_filter_groups(self):
        """
        Test filter on user groups
        """
        # This test expects a 200 since invalid filters are removed by the serializer
        self._test_user_list_filter(
            expected_status_code=200,
            groups=','.join(['1', '2', '3', '4'])
        )

    def test_111_user_list_filter_groups_list(self):
        """
        Test filter on user groups as list of groups
        """
        self._test_user_list_filter(groups=[1, 2, 3, 4])

    def test_113_user_create(self):
        """
        Test inviting a user
        """
        kc = KairnialClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.post(
            'users/',
            data=json.dumps({
                "users": [
                    {
                        "email": f"{self.email_uuid}@kairnialgroup.com",
                        "first_name": "Unit",
                        "last_name": "Test",
                        "language": "fr"
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
        kc = KairnialClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.get('users/0/')
        serializer = UserUUIDSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    def test_114_user_delete(self):
        kc = KairnialClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.delete(f'users/{self.created_user_id}')
        self.assertEqual(resp.status_code, 204)


class GroupTest(CommonTest):

    def setUp(self):
        super().setUp()
        self.group_name = str(uuid.uuid4())

    def test_100_group_list(self):
        """
        Test standard group list route
        """
        kc = KairnialClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.get('groups/')
        serializer = GroupSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    def test_101_group_list_filter_name(self):
        """
        Test standard group list route filtered by name
        """
        kc = KairnialClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.get('groups/', data={'name': 'test'})
        serializer = GroupSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    def test_112_group_get(self):
        """
        Test get user with ID
        """
        kc = KairnialClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.get('groups/48f944d3-bcb2-11e7-b7a1-fa163e5e5b59/')
        serializer = GroupSerializer(data=resp.json(), many=True)
        self.assertTrue(serializer.is_valid())

    def test_113_group_create(self):
        """
        Test inviting a user
        """
        kc = KairnialClient(
            access_token=self.access_token,
            client_id=self.client_id,
            project_id=self.project_id)
        resp = kc.post(
            'groups/',
            data=json.dumps({
                "name": self.group_name,
                "description": "Unit test description"
            }),
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(resp.status_code, 201)
