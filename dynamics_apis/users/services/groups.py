"""
Call to Kairnial Group Web Services
"""

from dynamics_apis.common.services import KairnialWSService


class KairnialGroup(KairnialWSService):
    """
    Service class for Kairnial Groups
    """
    service_domain = 'users'

    def list(self) -> []:
        """
        List users
        :return:
        """
        return self.call(
            action='getGroups',
            parameters=[{'allGroups': True}],
            use_cache=True)

    def create(self, group):
        """
        Create a group through Kairnial Web Services
        :param group: dynamics_apis.users.models.Group
        """
        return self.call(
            action='addGroup',
            parameters=[group.name, group.description],
            format='bool',
            use_cache=False
        )

    def add_users(self, group_id: int, user_list: [int]):
        """
        Add a list of users to a group
        """
        no_error = True
        for user in user_list:
            resp = self.call(
                action='addUserToGroup',
                parameters=[{'groupe': group_id, 'user': [user, ]}],
                format='bool',
                use_cache=False)
            no_error &= resp
        return no_error

    def remove_users(self, group_id: int, user_list: [int]):
        """
        Add a list of users to a group
        """
        no_error = True
        for user in user_list:
            resp = self.call(
                action='removeUserFromGroup',
                parameters=[{'groupe': group_id, 'user': [user, ]}],
                format='bool',
                use_cache=False)
            no_error &= resp
        return no_error

    def list_rights(self, group_id: int):
        """
        Displays the list of rights attached to this group
        """
        return self.call(
            service='aclmanager',
            action='getGroupsAcls',
            parameters=[{'group_uuid': group_id}],
            format='json',
            use_cache=True)

    def add_authorizations(self, group_id: str, authorizations: dict):
        """
        Add a list of authorizations to a group
        :param group_id: UUID of the group
        :param authorizations: dict with authorization uuid:type
        """
        no_error = True
        for authorization_uuid, authorization_name in authorizations.items():
            resp = self.call(
                service='aclmanager',
                action='addAclGrant',
                parameters=[
                    {
                        'item_type': 'group',
                        'item_uuid': group_id,
                        'acl_id': authorization_uuid,
                        'acl_type': authorization_name
                    }],
                format='json',
                use_cache=False)
            no_error &= resp.get('success', False)
        return no_error

    def remove_rights(self, group_id: int, authorizations: dict):
        """
        Add a list of authorizations to a group
        :param group_id: UUID of the group
        :param authorizations: dict with authorization uuid:type
        """
        no_error = True
        for authorization_uuid, authorization_name in authorizations.items():
            resp = self.call(
                service='aclmanager',
                action='removeRigthToGroup',
                parameters=[
                    {
                        'item_type': 'group',
                        'item_uuid': group_id,
                        'acl_id': authorization_uuid,
                        'acl_type': authorization_name
                    }],
                format='json',
                use_cache=False)
            no_error &= resp.get('success', False)
        return no_error
