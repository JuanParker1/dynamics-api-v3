"""
Serializers for Group
"""
from django.utils.translation import gettext as _
from rest_framework import serializers

from dynamics_apis.users.models.groups import Group


class GroupSerializer(serializers.Serializer):
    """
    Serializer for group object
    """
    id = serializers.UUIDField(source='guid', read_only=True)
    num_id = serializers.IntegerField(source='groups_id', read_only=True)
    name = serializers.CharField(label=_("Name of the group"), source='groups_label', read_only=True)
    description = serializers.CharField(label=_("Description of the group"), source='groups_desc', read_only=True)
    level = serializers.CharField(label=_("Description of the group"), source='groups_level', read_only=True)


class GroupQuerySerializer(serializers.Serializer):
    """
    Serializer for group filtering
    """
    name = serializers.CharField(label=_("Filter by group name"),
                                 help_text=_("Filter by group name. Case insensitive filter"),
                                 required=False)


class GroupAddUserSerializer(serializers.Serializer):
    """
    Serializer for user addition or removal to group
    """
    users = serializers.ListField(label=_("List of numerical user IDs"),
                                  help_text=_("List of user IDs to add to group"),
                                  child=serializers.IntegerField(),
                                  required=True)

class GroupAddAuthorizationSerializer(serializers.Serializer):
    """
    Serializer for user addition or removal to group
    """
    authorizations = serializers.DictField(label=_("List of ofauthorization"),
                                  help_text=_("List of UUID: type of authorization key:value"),
                                  required=True)


class GroupCreationSerializer(serializers.Serializer):
    """
    Serializer for group creation
    """
    name = serializers.CharField(
        label=_("Name of the group"),
        help_text=_("Type the name of your group"))
    description = serializers.CharField(label=_("Description of the group"), required=False,
                                        help_text=_("Type the description of your group"))

    def create(self, validated_data):
        """
        Create a new Group instance
        """
        return Group(
            name=validated_data['name'],
            description=validated_data.get('description', '')
        )

    def update(self, instance, validated_data):
        """
        Update instane values
        """
        instance.name = validated_data['name']
        instance.description = validated_data.get('description', instance.description)
        return instance


class RightSerializer(serializers.Serializer):
    legacy_rights = serializers.ListField(
        label=_("List of legacy rights"),
        help_text=_("List of legacy rights associated with the group"),
        child=serializers.IntegerField(), source='acls')
    rights = serializers.ListField(
        label=_("List of rights"),
        help_text=_("List of rights associated with the group"),
        child=serializers.CharField(), source='acl_links')
    modules = serializers.ListField(
        label=_("List of activated modules"),
        help_text=_("List of modules activated on the group"),
        child=serializers.CharField())

