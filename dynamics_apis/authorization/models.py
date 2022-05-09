"""
Kairnial authorization models
"""
from dynamics_apis.authorization.services import KairnialACL, KairnialModule


class ACL:

    @classmethod
    def list(cls, client_id: str, token: str, project_id: str,
             domain: str = None, search: str = None, user_id: str = None):
        """
        List Kairnial authorizations
        """
        ka = KairnialACL(client_id=client_id, token=token, user_id=user_id, project_id=project_id)
        acl_list = ka.list().get('acls')
        if domain:
            acl_list = [acl for acl in acl_list if acl['acl_type'].split(':')[0] == domain]
        if search:
            acl_list = [acl for acl in acl_list if search in f"{acl['description']}|{acl['acl_type']}"]
        return acl_list


class Module:

    @classmethod
    def list(cls, client_id: str, token: str, project_id: str, search: str = None, user_id: str = None):
        """
        List Kairnial authorizations
        """
        km = KairnialModule(
            client_id=client_id,
            token=token,
            user_id=user_id,
            project_id=project_id)
        module_list = km.list().get('modules')
        if search:
            module_list = [ml for ml in module_list if search in f"{ml['title']}|{ml['subtitle']}"]
        return module_list
