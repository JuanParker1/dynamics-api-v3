"""
Kairnial User serializer classes
"""

from django.utils.translation import gettext as _
from rest_framework import serializers

from dynamics_apis.users.serializers.groups import GroupSerializer


class UserCreationSerializer(serializers.Serializer):
    """
    Serializer for user creation
    """
    first_name = serializers.CharField(label=_("User first name"), required=True)
    last_name = serializers.CharField(label=_("User last name"), required=True)
    email = serializers.CharField(label=_("User email address"), required=True)


class ProjectMemberSerializer(serializers.Serializer):
    """
    Serializer for project members
    """
    id = serializers.IntegerField(label=_("User unique ID"), read_only=True, source='account_id')
    email = serializers.CharField(label=_("User email"), required=True, source='account_email')
    full_name = serializers.CharField(label=_("User full name"), required=True, source='account_firstname')
    archived = serializers.CharField(label=_("User has been archived"), required=False, source='account_achive',
                                     default=0)


class ProjectMemberCountSerializer(serializers.Serializer):
    """
    Serializer for number of users on a project
    """
    count = serializers.IntegerField(label=_("Number of users on this project"), read_only=True, source='nbUsers')


class UserSerializer(UserCreationSerializer):
    """
    User object serializer
    """
    id = serializers.IntegerField(label=_("User unique ID"), read_only=True)
    fullname = serializers.CharField(label=_("User full name"), read_only=True)
    status: serializers.CharField(label=_("User status"), read_only=True)
    last_connect_time = serializers.DateTimeField(label=_("Date of last connection"),
                                                  read_only=True, required=False)
    expiration_time = serializers.IntegerField(label=_("Time in days before account expiration"),
                                               default=0,
                                               read_only=True)
    creation_time = serializers.DateTimeField(label=_("Date of last connection"), read_only=True)
    update_time = serializers.DateTimeField(label=_("Date of last connection"), read_only=True)


class SelfSerializer(UserSerializer):
    """
    Serializer for current user
    """
    uuid = serializers.UUIDField(label=_("User universal identifier"), read_only=True,
                                 source='account_uuid')


class UserSimpleSerializer(serializers.Serializer):
    """
    Serializer for simple user
    """
    id = serializers.IntegerField(label=_("User unique ID"), read_only=True)
    email = serializers.CharField(label=_("User email address"), read_only=True)


class UserStatSerializer(serializers.Serializer):
    """
    Serializer for user stats
    """
    user = UserSerializer()
    count_pins = serializers.IntegerField(label=_("Number of defects created by user"), default=0,
                                          read_only=True)
    count_forms = serializers.IntegerField(label=_("Number of forms created by user"), default=0,
                                           read_only=True)
    count_connect = serializers.IntegerField(label=_("Number of user connections"), default=0,
                                             read_only=True)
    last_connect = serializers.IntegerField(label=_("Did the user connect once"), default=0,
                                            read_only=True)


class UserQuerySerializer(serializers.Serializer):
    """
    Serializer for user filtering
    """
    full_name = serializers.CharField(label=_("Full name case insensitive content filter"),
                                      help_text=_("Filter by user full name. Case insensitive content filter"),
                                      read_only=True,
                                      required=False)
    email = serializers.CharField(label=_("email case insensitive content filter"),
                                  help_text=_("Filter by user email. Case insensitive content filter"),
                                  required=False)
    archived = serializers.BooleanField(label=_("Boolean filter on archived status"),
                                        help_text=_("Is user archived, 0 or 1"), required=False)
    groups = serializers.CharField(label=_("List users for given numerical group IDs separated by a comma"),
                                   required=False)


class UserGroupSerializer(serializers.Serializer):
    """
    Serializer for list of groups for user
    """
    group_ids = serializers.ListField(
        label=_("list of group IDs"),
        help_text=_("List of numeric group IDs"),
        child=serializers.IntegerField()
    )


class UserInviteSerializer(serializers.Serializer):
    """
    Serializer for user invitation
    """
    email = serializers.CharField(
        label=_('User email'),
        help_text=_('User identifier and used to send invite'),
        required=True,
    )
    first_name = serializers.CharField(
        label=_('User first name'),
        help_text=_('First name for user. If not provided, deduced from email'),
        required=False,
        source='firstname'
    )
    last_name = serializers.CharField(
        label=_('User last name'),
        help_text=_('Last name for user. If not provided, deduced from email'),
        required=False,
        source='lastname'
    )
    language = serializers.ChoiceField(
        label=_('User language'),
        help_text=_('Interface language for user'),
        choices=['en', 'fr', 'de', 'es'],
        source='lng'
    )


class UserMultiInviteSerializer(serializers.Serializer):
    users = UserInviteSerializer(
        label=_('List of users'),
        help_text=_('List of users to invite'),
        many=True,
        required=True
    )


class UserInviteResponseSerializer(serializers.Serializer):
    admin_confirmation = serializers.BooleanField(
        label=_('Admin confirmation needed'),
        help_text=_('User is invited but the project admin needs to confirm the invitation'),
        read_only=True,
        source='needsAdminConfirmation'
    )
    already_invited = serializers.BooleanField(
        label=_('User is already invited'),
        help_text=_('User has already been sent an invitation'),
        read_only=True,
        source='alreadyInvited'
    )
    email_sent = serializers.BooleanField(
        label=_('Invitation email sent'),
        help_text=_('An invitation email has been sent to the user'),
        read_only=True,
        source='emailSent'
    )
    created = serializers.BooleanField(
        label=_('User created'),
        help_text=_('User has been created'),
        read_only=True,
        source='userHasBeenCreated'
    )
    creation_needed = serializers.BooleanField(
        label=_('Creation needed'),
        help_text=_('User needs to be created'),
        read_only=True,
        source='needToCreateUser'
    )
    user = ProjectMemberSerializer(
        label=_('Created user'),
        help_text=_('User details')
    )


class UserMultiInviteResponseSerializer(serializers.Serializer):
    users=UserInviteResponseSerializer(many=True)
    groups=GroupSerializer(many=True)