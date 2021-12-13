"""
Kairnial authorization models
"""
from dynamics_apis.authorization.services import KairnialACL


class ACL:

    @classmethod
    def list(cls, client_id: str, token: str, project_id: str, domain: str = None, search: str = None):
        """
        List Kairnial authorizations
        """
        ka = KairnialACL(client_id=client_id, token=token, project_id=project_id)
        acl_list = ka.list().get('acls')
        if domain:
            acl_list = [l for l in acl_list if l['acl_type'].split(':')[0] == domain]
        if search:
            acl_list = [l for l in acl_list if search in f"{l['description']}|{l['acl_type']}"]
        return acl_list