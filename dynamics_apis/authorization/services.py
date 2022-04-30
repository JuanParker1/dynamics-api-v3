"""
Services for Kairnial Authorization services
"""

from dynamics_apis.common.services import KairnialWSService


class KairnialACL(KairnialWSService):
    """
    Service class for Kairnial Groups
    """
    service_domain = 'aclmanager'

    def list(self) -> []:
        """
        List access rights
        :return:
        """
        return self.call(
            action='getAclGrants',
            use_cache=True)


class KairnialModule(KairnialWSService):
    """
    Service class for Kairnial Groups
    """
    service_domain = 'aclmanager'

    def list(self) -> []:
        """
        List access rights
        :return:
        """
        return self.call(
            action='getModules',
            use_cache=True)
