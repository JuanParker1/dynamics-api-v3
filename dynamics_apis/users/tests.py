import random
import string

from dynamics_apis.common.tests import CommonTest, KairnialClient
from .serializers.users import UserUUIDSerializer


class UserTest(CommonTest):
    """
    Test user routes
    """

    def test_user_list(self):
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

    def test_user_list_filter_archived_false(self):
        """
        Test unarchived user
        """
        self._test_user_list_filter(archived=False)

    def test_user_list_filter_archived_true(self):
        """
        Test archived user
        """
        self._test_user_list_filter(archived=True)

    def test_user_list_filter_email(self):
        """
        Test user email filter
        """
        self._test_user_list_filter(email='me@test.com')

    def test_user_list_filter_number_email(self):
        """
        Test user email filter with a number as argument
        """
        self._test_user_list_filter(email=1)

    def test_user_list_filter_email_injection(self):
        """
        Test user email filter with a SQL injection pattern
        """
        self._test_user_list_filter(email="me \" OR 1")

    def test_user_list_filter_email_too_long(self):
        """
        Test user email filter with a very long filter
        """
        letters = string.ascii_letters + string.digits
        email = ''.join(random.choice(letters) for i in range(10000))
        self._test_user_list_filter(email=email)

    def test_user_list_filter_full_name(self):
        """
        Test user full_name filter
        """
        self._test_user_list_filter(full_name="I am a full name")

    def test_user_list_filter_full_name_number(self):
        """
        Test user full_name filter with number as argument
        """
        self._test_user_list_filter(full_name=1)

    def test_user_list_filter_groups(self):
        """
        Test filter on user groups
        """
        # This test expects a 200 since invalid filters are removed by the serializer
        self._test_user_list_filter(
            expected_status_code=200,
            groups=','.join(['1','2','3','4'])
        )

    def test_user_list_filter_groups_list(self):
        """
        Test filter on user groups as list of groups
        """
        self._test_user_list_filter(groups=[1,2,3,4])

    def test_user_get(self):
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
