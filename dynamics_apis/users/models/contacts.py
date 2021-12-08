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
    def list(cls, client_id: str, token: str, project_id: str, filters: dict = None) -> []:
        """
        Get a list of users for a project
        :param client_id: ClientID Token
        :param token: Access token
        :param project_id: Project RGOC Code
        :param filters: Dict of filters
        :return:
        """
        parameters = [{key: value} for key, value in filters.items()]
        kc = KairnialContact(client_id=client_id, token=token, project_id=project_id)
        contacts = kc.list(parameters=parameters).get('items')
        return contacts

    @staticmethod
    def create(client_id: str, token: str, project_id: str, serialized_data: dict):
        """
        Create a group through Kairnial Web services call
        """
        kc = KairnialContact(client_id=client_id, token=token, project_id=project_id)
        return kc.create(serialized_data)

