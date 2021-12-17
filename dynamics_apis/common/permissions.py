"""
Check permissions
"""
from rest_framework import permissions


class KairnialUserPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method == 'POST':
            return True

        else:
            return request.user == obj or request.user.is_superuser
