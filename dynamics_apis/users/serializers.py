"""
Kairnial User serializer classes
"""
from django.utils.translation import ugettext as _
from rest_framework import serializers


class UserCreationSerializer(serializers.Serializer):
    first_name = serializers.CharField(label=_("User first name"), required=True)
    last_name = serializers.CharField(label=_("User last name"), required=True)
    email = serializers.CharField(label=_("User email address"), required=True)



class ProjectMemberSerializer(serializers.Serializer):
    id = serializers.IntegerField(label=_("User unique ID"), read_only=True, source='account_id')
    email = serializers.CharField(label=_("User email"), required=True, source='account_email')
    full_name = serializers.CharField(label=_("User full name"), required=True, source='account_firstname')
    archived = serializers.CharField(label=_("User has been archived"), required=False, source='account_achive', default=0)


class UserSerializer(UserCreationSerializer):
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
    uuid = serializers.UUIDField(label=_("User universal identifier"), read_only=True,
                                 source='account_uuid')


class UserSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField(label=_("User unique ID"), read_only=True)
    email = serializers.CharField(label=_("User email address"), read_only=True)


class UserStatSerializer(serializers.Serializer):
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
    full_name = serializers.CharField(label=_("Full name case insensitive content filter"),
                                      help_text=_("Filter by user full name. Case insensitive content filter"),
                                      read_only=True,
                                      required=False)
    email = serializers.CharField(label=_("email case insensitive content filter"),
                                  help_text=_("Filter by user email. Case insensitive content filter"),
                                  required=False)
    status = serializers.ChoiceField(label=_("status case insensitive exact filter"),
                                     help_text=_("status case insensitive exact filter"),
                                     choices=['running', 'walking', 'standing'], required=False)
    groups = serializers.CharField(label=_("List users for given numerical group IDs separated by a comma"),
                                   required=False)