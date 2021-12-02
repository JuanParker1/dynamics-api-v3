"""
Kairnial user model classes
"""

from django.db import models
from .services import KairnialUser

# Create your models here.
class User:
    """
    Kairnial user class
    """
    id = 0
    uuid = ''
    firstname = '',
    lastname = ''
    fullname = ''
    email = ''
    status: 'running'
    count_pins = 0
    count_forms = 0
    count_connect = 0
    last_connect = 0
    last_connect_time = ''
    expiration_time = 0
    creation_time = ''
    update_time = ''

    @staticmethod
    def list(client_id: str, token: str, project_id: str, filters: dict: {}) -> []:
        """
        Get a list of users for a project
        :param client_id:
        :param token:
        :param project:
        :param filters: Dict of filters
        :return:
        """
        users = None
        ku = KairnialUser(client_id=client_id, token=token, project_id=project_id)
        if 'groups' in filters:
            try:
                list_of_groups = [int(a.strip()) for a in filters.get('groups').split(',')]
                users = ku.list_for_groups(list_of_groups=list_of_groups)
            except ValueError:
                return None
        else:
            return ku.list().get('users')
        manual_filters = set(filters.keys()) & set(['full_name', 'email'])
        for m in manual_filters:
            users = [u for u in users if filters.get('m') in getattr(u, m, '').lower()]
        if 'archived' in filters:
            users = [u for u in users if getattr(u, 'archive, '').lower()]

