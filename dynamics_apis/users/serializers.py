"""
Kairnial User serializer classes
"""
from django.utils.translation import ugettext as _
from rest_framework import serializers


class KUserCreationSerializer(serializers.Serializer):
    firstname = serializers.CharField(label=_("User first name"), required=True)
    lastname = serializers.CharField(label=_("User last name"), required=True)
    email = serializers.CharField(label=_("User email address"), required=True)


class KUserSerializer(KUserCreationSerializer):
    id = serializers.IntegerField(label=_("User unique ID"), read_only=True)
    uuid = serializers.UUIDField(label=_("User universal identifier"), read_only=True)
    fullname = serializers.CharField(label=_("User full name"), read_only=True)
    status: serializers.CharField(label=_("User status"), read_only=True)
    last_connect_time = serializers.DateTimeField(label=_("Date of last connection"),
                                                  read_only=True, required=False)
    expiration_time = serializers.IntegerField(label=_("Time in days before account expiration"),
                                               default=0,
                                               read_only=True)
    creation_time = serializers.DateTimeField(label=_("Date of last connection"), read_only=True)
    update_time = serializers.DateTimeField(label=_("Date of last connection"), read_only=True)


class KUserSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField(label=_("User unique ID"), read_only=True)
    email = serializers.CharField(label=_("User email address"), read_only=True)


class KUserStatSerializer(serializers.Serializer):
    user = KUserSerializer()
    count_pins = serializers.IntegerField(label=_("Number of defects created by user"), default=0,
                                          read_only=True)
    count_forms = serializers.IntegerField(label=_("Number of forms created by user"), default=0,
                                           read_only=True)
    count_connect = serializers.IntegerField(label=_("Number of user connections"), default=0,
                                             read_only=True)
    last_connect = serializers.IntegerField(label=_("Did the user connect once"), default=0,
                                            read_only=True)


class KUserQuerySerializer(serializers.Serializer):
    firstname = serializers.CharField(label=_("First name case insensitive content filter"),
                                      required=False)
    lastname = serializers.CharField(label=_("Last name case insensitive content filter"),
                                     required=False)
    email = serializers.CharField(label=_("email case insensitive content filter"), required=False)
    status = serializers.ChoiceField(label=_("status case insensitive exact filter"),
                                     choices=['running', 'walking', 'standing'], required=False)
