"""
Serializers for the GraphQL implementation
"""
from django.utils.translation import gettext as _
from rest_framework import serializers
from dynamics_apis.projects.serializers import ProjectSerializer
from dynamics_apis.users.serializers.users import ProjectMemberSerializer
from dynamics_apis.users.serializers.groups import GroupSerializer
from dynamics_apis.users.serializers.contacts import ContactSerializer, ContactQuerySerializer
from dynamics_apis.users.models.users import User
from dynamics_apis.users.models.groups import Group
from dynamics_apis.users.models.contacts import Contact


class ProjectGraphQLSerializer(ProjectSerializer):
    """
    Starting from ProjectSerializer and expanding to relations
    """
    client_id = serializers.CharField(label=_("Injected client_id for technical use"))
    users = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()

    def get_users(self, obj):
        """
        List project users
        """
        user_list = User.list(
            client_id=obj.get('client_id'),
            token=obj.get('token'),
            project_id=obj.get('g_nom'),
            filters={}
        )
        return ProjectMemberSerializer(user_list, many=True).data

    def get_groups(self, obj):
        """
        List project groups
        """
        group_list = Group.list(
            client_id=obj.get('client_id'),
            token=obj.get('token'),
            project_id=obj.get('g_nom')
        )
        return GroupSerializer(group_list, many=True).data

    def get_contacts(self, obj):
        """
        List project groups
        """
        # Putting default values
        filters = ContactQuerySerializer(data={})
        filters.is_valid()
        print(filters.validated_data)
        contacts_list = Contact.list(
            client_id=obj.get('client_id'),
            token=obj.get('token'),
            project_id=obj.get('g_nom'),
            filters=filters.validated_data
        )
        print(contacts_list)
        return ContactSerializer(contacts_list, many=True).data
