"""
Contact serializers
"""
from django.utils.translation import ugettext as _
from rest_framework import serializers


class ContactQuerySerializer(serializers.Serializer):
    """
    Serializer for contact filtering
    """
    type = serializers.ChoiceField(
        label=_("Type of contact"),
        help_text=_("Type of contact in contact / company"),
        choices=['entreprise', 'contact'],
        default='contact'
    )
    search = serializers.CharField(
        label=_("Name case insensitive content filter"),
        help_text=_("Filter by contact name. Case insensitive content filter"),
        required=False)
    ids = serializers.ListSerializer(
        label=_("Search for specific contact ids"),
        help_text=_("Search in name email and other name"),
        child=serializers.IntegerField(),
        required=False
    )
    created_start = serializers.DateField(
        label=_("Filter on contacts created after this date"),
        help_text=_("Date format YYYY-MM-DD"),
        required=False
    )
    created_end = serializers.DateField(
        label=_("Filter on contacts created before this date"),
        help_text=_("Date format YYYY-MM-DD"),
        required=False
    )
    update_start = serializers.DateField(
        label=_("Filter on contacts updated after this date"),
        help_text=_("Date format YYYY-MM-DD"),
        required=False
    )
    update_end = serializers.DateField(
        label=_("Filter on contacts updated before this date"),
        help_text=_("Date format YYYY-MM-DD"),
        required=False,
    )


class ContactCreationSerializer(serializers.Serializer):
    """
    Serializer for creator in contact response
    """
    id = serializers.IntegerField(
        label=_('User ID'),
        help_text=_("User technical ID"), read_only=True,
        source='contact_created_by_id'
    )
    first_name = serializers.CharField(label=_("User first name"), read_only=True,
                                       source='contact_created_by_firstname')
    last_name = serializers.CharField(label=_("User last name"), read_only=True,
                                      source='contact_created_by_lastname')
    email = serializers.CharField(label=_("User email address"), read_only=True,
                                  source='contact_created_by_email')


class ContactSerializer(serializers.Serializer):
    """
    Serializer for contact list and retrieve
    """
    id = serializers.IntegerField(
        label=_('Contact technical ID'),
        help_text=_("Contact numerical ID"),
        read_only=True,
        source='contact_id'
    )
    uuid = serializers.UUIDField(
        label=_('Contact unique ID'),
        help_text=_("Contact unique ID"),
        read_only=True,
        source='contact_uuid'
    )
    link_to_defects = serializers.BooleanField(
        label=_("Associate contact with defects"),
        help_text=_("This contact can be associated with defects"),
        read_only=True,
        source='contact_'
    )
    company_name = serializers.CharField(
        label=_("Contact company name"),
        help_text=_("Company name for contact"),
        read_only=True,
        source='contact_company_name'
    )
    category = serializers.CharField(
        label=_("Contact category"),
        help_text=("Contact category name"),
        read_only=True,
        source='contact_category'
    )
    short_name = serializers.CharField(
        label=_("Contact short name"),
        help_text=("Contact short name"),
        read_only=True,
        source='contact_quick_name'
    )
    name = serializers.CharField(
        label=_("Contact name"),
        help_text=("Contact name"),
        read_only=True,
        source='contact_name'
    )
    alternative_name = serializers.CharField(
        label=_("Contact alternative name"),
        help_text=("Contact alternative name"),
        read_only=True,
        source='contact_other_name'
    )
    address = serializers.CharField(
        label=_("Contact address"),
        help_text=("Contact address street name"),
        read_only=True,
        source='contact_address'
    )
    zipcode = serializers.CharField(
        label=_("Contact zipcode"),
        help_text=("Contact address zip code"),
        read_only=True,
        source='contact_zip'
    )
    city = serializers.CharField(
        label=_("Contact city"),
        help_text=("Contact address city"),
        read_only=True,
        source='contact_city'
    )
    county = serializers.CharField(
        label=_("Contact county"),
        help_text=("Contact county name"),
        read_only=True,
        source='contact_county'
    )
    country = serializers.CharField(
        label=_("Contact country"),
        help_text=("Contact country name"),
        read_only=True,
        source='contact_country'
    )
    phone = serializers.CharField(
        label=_("Contact phone number"),
        help_text=("Contact phone number"),
        read_only=True,
        source='contact_phone'
    )
    direct_phone = serializers.CharField(
        label=_("Contact direct phone number"),
        help_text=("Contact direct phone number"),
        read_only=True,
        source='contact_direct_phone'
    )
    fax = serializers.CharField(
        label=_("Contact fax number"),
        help_text=("Contact fax number"),
        read_only=True,
        source='contact_fax'
    )
    mobile = serializers.CharField(
        label=_("Contact mobile number"),
        help_text=("Contact mobile number"),
        read_only=True,
        source='contact_mobile'
    )
    url = serializers.CharField(
        label=_("Contact website url"),
        help_text=("Contact website url"),
        read_only=True,
        source='contact_url'
    )
    email = serializers.CharField(
        label=_("Contact e-mail address"),
        help_text=("Contact e-mail address"),
        read_only=True,
        source='contact_email'
    )
    description = serializers.CharField(
        label=_("Contact description"),
        help_text=("Contact description"),
        read_only=True,
        source='contact_description'
    )
    external_reference = serializers.CharField(
        label=_("Contact code"),
        help_text=("Contact code"),
        read_only=True,
        source='contact_fax'
    )
    created_at = serializers.DateTimeField(
        label=_("Contact creation time"),
        help_text=("Contact creation time"),
        read_only=True,
        source='creation_time'
    )
    updated_at = serializers.DateTimeField(
        label=_("Contact update time"),
        help_text=("Contact update time"),
        read_only=True,
        source='creation_time'
    )
    created_by = ContactCreationSerializer(
        label=_("Contact created by"),
        read_only=True,
        source='contact_created_by_user'
    )