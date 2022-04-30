"""
Kairnial User serializer classes
"""

from django.utils.translation import gettext as _
from rest_framework import serializers


class UserCreationSerializer(serializers.Serializer):
    """
    Serializer for user creation
    """
    first_name = serializers.CharField(label=_("User first name"), required=True)
    last_name = serializers.CharField(label=_("User last name"), required=True)
    email = serializers.CharField(label=_("User email address"), required=True)


class UserUUIDSerializer(serializers.Serializer):
    """
    Serializer for another kind of user with UUID
    """
    id = serializers.UUIDField(
        label=_("User numeric ID"),
        help_text=_('Numeric ID for the user, not a username'),
        read_only=True,
        source='account_id')
    uuid = serializers.UUIDField(
        label=_("User unique ID"),
        help_text=_('Unique ID for the user, not a username'),
        read_only=True,
        source='account_uuid')
    email = serializers.CharField(
        label=_("User email"),
        help_text=_("e-mail for user, equivalent to username"),
        read_only=True, source='account_email')
    first_name = serializers.CharField(
        label=_("User first name"),
        help_text=_("User first name"),
        read_only=True, source='account_firstname')
    last_name = serializers.CharField(
        label=_("User last name"),
        help_text=_("User last name"),
        read_only=True,
        source='account_lastname')
    expires = serializers.BooleanField(
        label=_("account expires"),
        help_text=_("Indicator if account is set to expire"),
        read_only=True, source='account_expiration')
    archive = serializers.BooleanField(
        label=_("archived account"),
        help_text=_("User account has been archived"),
        read_only=True, source='account_archive')
    title = serializers.CharField(
        label=_("User title"),
        help_text=_("Title of the user"),
        read_only=True, source='user_gender')


class ProjectMemberSerializer(serializers.Serializer):
    """
    Serializer for project members
    """
    id = serializers.IntegerField(label=_("User unique ID"), read_only=True, source='account_id')
    email = serializers.CharField(label=_("User email"), required=True, source='account_email')
    full_name = serializers.CharField(label=_("User full name"), required=True,
                                      source='account_firstname')
    archived = serializers.CharField(label=_("User has been archived"), required=False,
                                     source='account_achive',
                                     default=0)


class ProjectMemberCountSerializer(serializers.Serializer):
    """
    Serializer for number of users on a project
    """
    count = serializers.IntegerField(label=_("Number of users on this project"), read_only=True,
                                     source='nbUsers')


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
    full_name = serializers.CharField(
        label=_("Full name case insensitive content filter"),
        help_text=_("Filter by user full name. Case insensitive content filter"),
        read_only=True,
        required=False,
        source='account_firstname')
    email = serializers.CharField(
        label=_("email case insensitive content filter"),
        help_text=_("Filter by user email. Case insensitive content filter"),
        required=False,
        source='account_email')
    archived = serializers.BooleanField(
        label=_("Boolean filter on archived status"),
        help_text=_("Is user archived, 0 or 1"),
        required=False,
        source='account_achive')
    groups = serializers.ListField(
        label=_("List users for given numerical group IDs"),
        child=serializers.IntegerField(),
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


class InvitedUserSerializer(serializers.Serializer):
    id = serializers.UUIDField(
        label=_("User unique ID"),
        help_text=_('Unique ID for the user, not a username'),
        read_only=True,
        source='_unique_identifier')
    email = serializers.CharField(
        label=_("User email"),
        help_text=_("e-mail for user, equivalent to username"),
        required=True, source='_email')
    first_name = serializers.CharField(
        label=_("User first name"),
        help_text=_("User first name"),
        required=True, source='_firstName')
    last_name = serializers.CharField(
        label=_("User last name"),
        help_text=_("User last name"),
        required=True,
        source='_lastName')
    expires = serializers.BooleanField(
        label=_("account expires"),
        help_text=_("Indicator if account is set to expire"),
        required=True, source='_account_expires')
    archive = serializers.BooleanField(
        label=_("archived account"),
        help_text=_("User account has been archived"),
        required=True, source='_archive')
    language = serializers.CharField(
        label=_("User language"),
        help_text=_("Language of the user interface"),
        required=False, source='_language',
        default=0)


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
    user = InvitedUserSerializer(
        label=_('Created user'),
        help_text=_('User details')
    )


class UserMultiInviteResponseSerializer(serializers.Serializer):
    users = UserInviteResponseSerializer(many=True)
