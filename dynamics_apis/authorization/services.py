"""
Services for Kairnial Authorization services
"""

from dynamics_apis.common.services import KairnialWSService


class KairnialACLService(KairnialWSService):
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

    def list_transmitters(self) -> []:
        """
        List defect transmitters
        """
        return self.call(
            service='reserves',
            action='getAllowedEmitters',
            parameters=[{}],
            use_cache=True
        )


class KairnialModuleService(KairnialWSService):
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
