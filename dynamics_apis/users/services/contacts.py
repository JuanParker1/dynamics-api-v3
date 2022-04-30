"""
Call to Kairnial Web Services
"""
from dynamics_apis.common.services import KairnialWSService


class KairnialContact(KairnialWSService):
    """
    Service class for Kairnial Contacts
    """
    service_domain = 'contacts'
    item_type = 'contact'

    def list(self, parameters: list=None) -> []:
        """
        List contacts
        :param parameters: search and filter parameters
        :return:
        """
        if not parameters:
            parameters = [{}, ]
        return self.call(
            action='getItem',
            parameters=parameters,
            use_cache=True
        )

    def create(self, contact_serializer):
        """
        Create a group through Kairnial Web Services
        :param contact_serializer: validated data from a ContactCreationSerializer
        """
        return self.call(
            action='addCompany',
            parameters=[contact_serializer, ],
            out_format='int',
        )

    def update(self, pk, contact_update_serializer):
        """
        Update a Kairnial Contact
        :param contact_update_serializer: validated data from a ContactUpdateSerializer
        :param pk: UUID of the contact
        """
        contact_update_serializer['guid'] = pk
        return self.call(
            action='updateCompany',
            parameters=[contact_update_serializer, ],
            out_format='int'
        )

    def delete(self, pk: int):
        """
        Archive a Kairnial contact
        :param pk: Numerical ID of the contact
        """
        return self.call(
            action='archiveEntreprise',
            parameters=[{'contactid': pk}],
            out_format='int'
        )
