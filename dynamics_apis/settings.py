KAIRNIAL_PROJECT_ENVIRONMENTS = [
    'default',
]
KIARNIAL_AUTHENTICATION_SCOPES = [
    'login-token',
    'project-list',
    'direct-login'
]

import os
def load_key(path):
    with open(path, 'r') as key:
        return key.read()