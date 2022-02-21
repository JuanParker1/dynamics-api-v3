"""
Serializers for the GraphQL implementation
"""
from rest_framework import serializers

from dynamics_apis.projects.serializers import ProjectSerializer
from dynamics_apis.users.models.contacts import Contact
from dynamics_apis.users.models.groups import Group
from dynamics_apis.users.models.users import User
from dynamics_apis.users.serializers.contacts import ContactSerializer, ContactQuerySerializer
from dynamics_apis.users.serializers.groups import GroupSerializer
from dynamics_apis.users.serializers.users import ProjectMemberSerializer


class LazyContactsField(serializers.Field):
    """
    List project contacts
    """

    def to_representation(self, obj):
        if obj.get('selected'):
            contacts_list = Contact.list(
                client_id=obj.get('client_id'),
                token=obj.get('token'),
                project_id=obj.get('project_id'),
                filters=obj.get('filters')
            )
            return ContactSerializer(contacts_list, many=True).data
        return []


class LazyGroupsField(serializers.Field):

    def to_representation(self, obj):
        """
        List project groups
        """
        if obj.get('selected'):
            group_list = Group.list(
                client_id=obj.get('client_id'),
                token=obj.get('token'),
                project_id=obj.get('project_id'),
                filters=obj.get('filters')
            )
            return GroupSerializer(group_list, many=True).data
        return []


class LazyUsersField(serializers.Field):

    def to_representation(self, obj):
        """
        List project users
        """
        if obj.get('selected'):
            user_list = User.list(
                client_id=obj.get('client_id'),
                token=obj.get('token'),
                project_id=obj.get('project_id'),
                filters=obj.get('filters')
            )
            return ProjectMemberSerializer(user_list, many=True).data
        else:
            return []


class ProjectGraphQLSerializer(ProjectSerializer):
    """
    Starting from ProjectSerializer and expanding to relations
    """
    users = LazyUsersField()
    groups = LazyGroupsField()
    contacts = LazyContactsField()
