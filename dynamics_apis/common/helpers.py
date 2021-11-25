"""
Common objects
"""
import os
import json

import jwt
import requests
from django.conf import settings
from django.contrib.auth import authenticate


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username
