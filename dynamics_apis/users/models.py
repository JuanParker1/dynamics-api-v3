"""
Kairnial user model classes
"""

from django.db import models


# Create your models here.
class KUser:
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

    def list(self, **filters):
        pass

