"""
Serializers for Kairnial Controls module
"""
import json

from django.utils.translation import gettext as _
from rest_framework import serializers


class ControlQuerySerializer(serializers.Serializer):
    """
    Serializer for folder query parameters
    """
    id = serializers.UUIDField(
        label=_("filter on ID"),
        help_text=_("retrieve control with given ID"),
        source='template_uuid',
        required=False
    )
    updated_before = serializers.DateField(
        label=_('folder updated before'),
        help_text=_('date of latest modification'),
        required=False,
        source='modification_end'
    )
    updated_after = serializers.DateField(
        label=_('folder updated after'),
        help_text=_('date of oldest modification'),
        required=False,
        source='modification_start'
    )
    created_before = serializers.DateField(
        label=_('folder created before'),
        help_text=_('date of latest creation'),
        required=False,
        source='creation_end'
    )
    created_after = serializers.DateField(
        label=_('folder created after'),
        help_text=_('date of oldest creation'),
        required=False,
        source='creation_start'
    )


class ControlTemplateElement(serializers.Serializer):
    """
    Serializer for template element
    """
    key = serializers.CharField(
        label=_('Element key'),
        help_text=_('Element key'),
        required=False
    )
    name = serializers.CharField(
        label=_('Element name'),
        help_text=_('Element name'),
        required=True
    )
    type = serializers.CharField(
        label=_('Element type'),
        help_text=_('Element type'),
        required=True
    )
    type = serializers.CharField(
        label=_('Element color'),
        help_text=_('color name'),
        required=False
    )
    default_value = serializers.CharField(
        label=_('Element color'),
        help_text=_('color name'),
        required=False
    )
    required = serializers.BooleanField(

    )

class ControlTemplateSerializer(serializers.Serializer):
    """
    Serializer for ControlTemplate
    """
    id = serializers.UUIDField(
        label=_("Control template ID"),
        help_text=_("UUID of the control template"),
        source='template_uuid',
        required=False
    )


{
		'notes_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9',
		'notes_id': '181',
		'title': 'CEA - Plafonds suspendus',
		'content': {
			'elements': [{
				'key': '',
				'name': 'Interfaces Amont',
				'type': 'S',
				'color': 'orange',
				'defaultValue': '',
				'required': '',
				'index': 1,
				'choices': '',
				'parentId': 1,
				'settings': {
					'eControl': {
						'niveau': '',
						'moyen': ''
					},
					'hidden': False
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Bon à fermer CET',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 23,
				'parentId': 1,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': '',
						'entreprise': '2'
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9',
				'fr': 'Bon à fermer CET'
			}, {
				'key': '',
				'name': 'Contrôle trait de niveau',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 3,
				'parentId': 1,
				'settings': {
					'eControl': {
						'niveau': 2,
						'moyen': ''
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Contrôle altimétries réseaux',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 4,
				'parentId': 1,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': ''
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Hygrométrie / Température',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 5,
				'parentId': 1,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': ''
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Contrôles en cours de travaux',
				'type': 'S',
				'color': 'orange',
				'defaultValue': '',
				'required': '',
				'index': 6,
				'choices': '',
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': '',
						'moyen': ''
					},
					'hidden': False
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Ossature primaire si bac acier',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 7,
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': 'Visuel'
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Nombre de suspentes',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 8,
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': 'Norme - DTU'
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Calepinage ossatures',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 9,
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': "Plan d'exe"
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Coloris des ossatures ',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 10,
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': 'Fiche produit validé'
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Coloris des dalles ou bacs',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 11,
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': 'Fiche produit validé'
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Hauteur sous fx plafond',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 12,
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': 'PROGRAMME CLIENT /CCTP'
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Bon à fermer (blanchiment)',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 13,
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': ''
					},
					'hidden': 0
				},
				'fr': 'Bon à fermer (blanchiment)',
				'editionGroupsIds': [],
				'visibilityGroupsIds': [],
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Percements pour terminaux',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 14,
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': ''
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Alignement des cornières',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 15,
				'parentId': 6,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': ''
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Essais',
				'type': 'S',
				'color': 'orange',
				'defaultValue': '',
				'required': '',
				'index': 16,
				'choices': '',
				'parentId': 16,
				'settings': {
					'eControl': {
						'niveau': '',
						'moyen': ''
					},
					'hidden': False
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Essais acoustiques',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 17,
				'parentId': 16,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': 'Notice acoustique marché'
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Contrôles finauxou Interface Aval',
				'type': 'S',
				'color': 'orange',
				'defaultValue': '',
				'required': '',
				'index': 18,
				'choices': '',
				'parentId': 18,
				'settings': {
					'eControl': {
						'niveau': '',
						'moyen': ''
					},
					'hidden': False
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Alignements réglages',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 19,
				'parentId': 18,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': 'Visuel '
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'Propreté des dalles',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 20,
				'parentId': 18,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': 'Visuel '
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': "Absence d'épaufrures",
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 21,
				'parentId': 18,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': 'Visuel '
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}, {
				'key': '',
				'name': 'OPR',
				'type': 'MC',
				'color': '',
				'defaultValue': '',
				'required': '',
				'index': 22,
				'parentId': 18,
				'settings': {
					'eControl': {
						'niveau': 0,
						'moyen': ''
					},
					'hidden': 0
				},
				'form_uuid': 'a7711e70-b5a8-11e8-9c8b-7d3c9035dcb9'
			}],
			'showOnlyCols': False,
			'groups': [],
			'settings': {
				'canCreateInstances': True,
				'colorizeSections': False,
				'hideStates': False,
				'allowLinkedPins': True
			}
		},
		'creation_date': '1578299370',
		'modification_date': '1578299370',
		'creator': 'Raphael Menard',
		'creator_email': 'raphael.menard@resolving.com',
		'creator_id': '31691',
		'category_label': 'Sans catégorie'
	}



class ControlInstanceSerializer(serializers.Serializer):
    """
    Serializer for ControlInstance
    """
    id = serializers.UUIDField(
        label=_("Control instance ID"),
        help_text=_("UUID of the control instance"),
        source='template_uuid',
        required=False
    )