"""
Kairnial authorization models
"""
from dynamics_apis.authorization.services import KairnialACLService, KairnialModuleService


class ACL:

    @classmethod
    def list(cls, client_id: str, token: str, project_id: str,
             domain: str = None, search: str = None, user_id: str = None):
        """
        List Kairnial authorizations
        """
        ka = KairnialACLService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        acl_list = ka.list().get('acls')
        if domain:
            acl_list = [l for l in acl_list if l['acl_type'].split(':')[0] == domain]
        if search:
            acl_list = [l for l in acl_list if search in f"{l['description']}|{l['acl_type']}"]
        return acl_list

    @classmethod
    def transmitters(cls, client_id: str, token: str, project_id: str, user_id: str = None):
        """
        List allowed defect transmitterrs
        """
        ka = KairnialACLService(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        return ka.list_transmitters()

class Module:

    @classmethod
    def list(cls, client_id: str, token: str, project_id: str, search: str = None, user_id: str = None):
        """
        List Kairnial authorizations
        """
        km = KairnialModuleService(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id)
        module_list = km.list().get('modules')
        if search:
            module_list = [l for l in module_list if search in f"{l['title']}|{l['subtitle']}"]
        return module_list