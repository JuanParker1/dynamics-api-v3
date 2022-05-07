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
            parameters=[{}],
            use_cache=True)

    def list_emittors(self) -> []:
        """
        List defect emittors
        """
        return self.call(
            service='reserves',
            action='getAllowedEmitters',
            parameters=[{}],
            use_cache=True
        )


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
            parameters=[{}],
            use_cache=True)