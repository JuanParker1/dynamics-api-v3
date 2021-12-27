"""
Kairnial user model classes
"""
from dynamics_apis.users.services.contacts import KairnialContact


# Create your models here.
class Contact:
    """
    Kairnial contact class
    """
    @staticmethod
    def list(client_id: str, token: str, project_id: str, filters: dict = None) -> []:
        """
        Get a list of contacts for a project
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param filters: Dict of filters
        :return:
        """
        parameters = [{key: value} for key, value in filters.items()]
        kc = KairnialContact(client_id=client_id, token=token, project_id=project_id)
        contacts = kc.list(parameters=parameters)
        if contacts:
            return contacts.get('items')
        return contacts

    @staticmethod
    def create(client_id: str, token: str, project_id: str, serialized_data: dict):
        """
        Create a contact through Kairnial Web services call
        """
        kc = KairnialContact(client_id=client_id, token=token, project_id=project_id)
        return kc.create(serialized_data)

    @staticmethod
    def update(client_id: str, token: str, project_id: str, pk: str, serialized_data: dict):
        """
        Update a contact through Kairnial Web services call
        """
        kc = KairnialContact(client_id=client_id, token=token, project_id=project_id)
        return kc.update(pk=pk, contact_update_serializer=serialized_data)

    @staticmethod
    def delete(client_id: str, token: str, project_id: str, pk: int):
        """
        Archive a contact
        """
        kc = KairnialContact(client_id=client_id, token=token, project_id=project_id)
        return kc.delete(pk=pk)