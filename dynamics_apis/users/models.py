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

    def list(self, client_id: str, token: str, project: str, **filters):
        """
        Get a list of users for a project
        :param client_id:
        :param token:
        :param project:
        :param filters:
        :return:
        """
        ku = KairnialUser(client_id=client_id, token=token, project=project)
        return ku.list()

