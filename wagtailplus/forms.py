#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains form class definitions.
"""
from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext as _


# ISO 3166 information from pycountry 1.10
# https://pypi.python.org/pypi/pycountry.
COUNTRIES = (
    ('AF', 'Islamic Republic of Afghanistan'),
    ('AL', 'Republic of Albania'),
    ('DZ', 'People\'s Democratic Republic of Algeria'),
    ('AD', 'Principality of Andorra'),
    ('AO', 'Republic of Angola'),
    ('AR', 'Argentine Republic'),
    ('AM', 'Republic of Armenia'),
    ('AT', 'Republic of Austria'),
    ('AZ', 'Republic of Azerbaijan'),
    ('BS', 'Commonwealth of the Bahamas'),
    ('BH', 'Kingdom of Bahrain'),
    ('BD', 'People\'s Republic of Bangladesh'),
    ('BY', 'Republic of Belarus'),
    ('BE', 'Kingdom of Belgium'),
    ('BJ', 'Republic of Benin'),
    ('BT', 'Kingdom of Bhutan'),
    ('BO', 'Plurinational State of Bolivia'),
    ('BQ', 'Bonaire, Sint Eustatius and Saba'),
    ('BA', 'Republic of Bosnia and Herzegovina'),
    ('BW', 'Republic of Botswana'),
    ('BR', 'Federative Republic of Brazil'),
    ('BG', 'Republic of Bulgaria'),
    ('BI', 'Republic of Burundi'),
    ('KH', 'Kingdom of Cambodia'),
    ('CM', 'Republic of Cameroon'),
    ('CV', 'Republic of Cape Verde'),
    ('TD', 'Republic of Chad'),
    ('CL', 'Republic of Chile'),
    ('CN', 'People\'s Republic of China'),
    ('CO', 'Republic of Colombia'),
    ('KM', 'Union of the Comoros'),
    ('CG', 'Republic of the Congo'),
    ('CR', 'Republic of Costa Rica'),
    ('CI', 'Republic of Côte d\'Ivoire'),
    ('HR', 'Republic of Croatia'),
    ('CU', 'Republic of Cuba'),
    ('CW', 'Curaçao'),
    ('CY', 'Republic of Cyprus'),
    ('DK', 'Kingdom of Denmark'),
    ('DJ', 'Republic of Djibouti'),
    ('DM', 'Commonwealth of Dominica'),
    ('EC', 'Republic of Ecuador'),
    ('EG', 'Arab Republic of Egypt'),
    ('SV', 'Republic of El Salvador'),
    ('GQ', 'Republic of Equatorial Guinea'),
    ('ER', 'the State of Eritrea'),
    ('EE', 'Republic of Estonia'),
    ('ET', 'Federal Democratic Republic of Ethiopia'),
    ('FJ', 'Republic of Fiji'),
    ('FI', 'Republic of Finland'),
    ('FR', 'French Republic'),
    ('GA', 'Gabonese Republic'),
    ('GM', 'Republic of the Gambia'),
    ('DE', 'Federal Republic of Germany'),
    ('GH', 'Republic of Ghana'),
    ('GR', 'Hellenic Republic'),
    ('GT', 'Republic of Guatemala'),
    ('GN', 'Republic of Guinea'),
    ('GW', 'Republic of Guinea-Bissau'),
    ('GY', 'Republic of Guyana'),
    ('HT', 'Republic of Haiti'),
    ('HN', 'Republic of Honduras'),
    ('HK', 'Hong Kong Special Administrative Region of China'),
    ('HU', 'Hungary'),
    ('IS', 'Republic of Iceland'),
    ('IN', 'Republic of India'),
    ('ID', 'Republic of Indonesia'),
    ('IR', 'Islamic Republic of Iran'),
    ('IQ', 'Republic of Iraq'),
    ('IL', 'State of Israel'),
    ('IT', 'Italian Republic'),
    ('JO', 'Hashemite Kingdom of Jordan'),
    ('KZ', 'Republic of Kazakhstan'),
    ('KE', 'Republic of Kenya'),
    ('KI', 'Republic of Kiribati'),
    ('KP', 'Democratic People\'s Republic of Korea'),
    ('KW', 'State of Kuwait'),
    ('KG', 'Kyrgyz Republic'),
    ('LV', 'Republic of Latvia'),
    ('LB', 'Lebanese Republic'),
    ('LS', 'Kingdom of Lesotho'),
    ('LR', 'Republic of Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Principality of Liechtenstein'),
    ('LT', 'Republic of Lithuania'),
    ('LU', 'Grand Duchy of Luxembourg'),
    ('MO', 'Macao Special Administrative Region of China'),
    ('MK', 'The Former Yugoslav Republic of Macedonia'),
    ('MG', 'Republic of Madagascar'),
    ('MW', 'Republic of Malawi'),
    ('MV', 'Republic of Maldives'),
    ('ML', 'Republic of Mali'),
    ('MT', 'Republic of Malta'),
    ('MH', 'Republic of the Marshall Islands'),
    ('MR', 'Islamic Republic of Mauritania'),
    ('MU', 'Republic of Mauritius'),
    ('MX', 'United Mexican States'),
    ('FM', 'Federated States of Micronesia'),
    ('MD', 'Republic of Moldova'),
    ('MC', 'Principality of Monaco'),
    ('ME', 'Montenegro'),
    ('MA', 'Kingdom of Morocco'),
    ('MZ', 'Republic of Mozambique'),
    ('MM', 'Republic of Myanmar'),
    ('NA', 'Republic of Namibia'),
    ('NR', 'Republic of Nauru'),
    ('NP', 'Federal Democratic Republic of Nepal'),
    ('NL', 'Kingdom of the Netherlands'),
    ('NI', 'Republic of Nicaragua'),
    ('NE', 'Republic of the Niger'),
    ('NG', 'Federal Republic of Nigeria'),
    ('NU', 'Niue'),
    ('MP', 'Commonwealth of the Northern Mariana Islands'),
    ('NO', 'Kingdom of Norway'),
    ('OM', 'Sultanate of Oman'),
    ('PK', 'Islamic Republic of Pakistan'),
    ('PW', 'Republic of Palau'),
    ('PS', 'the State of Palestine'),
    ('PA', 'Republic of Panama'),
    ('PG', 'Independent State of Papua New Guinea'),
    ('PY', 'Republic of Paraguay'),
    ('PE', 'Republic of Peru'),
    ('PH', 'Republic of the Philippines'),
    ('PL', 'Republic of Poland'),
    ('PT', 'Portuguese Republic'),
    ('QA', 'State of Qatar'),
    ('RW', 'Rwandese Republic'),
    ('WS', 'Independent State of Samoa'),
    ('SM', 'Republic of San Marino'),
    ('ST', 'Democratic Republic of Sao Tome and Principe'),
    ('SA', 'Kingdom of Saudi Arabia'),
    ('SN', 'Republic of Senegal'),
    ('RS', 'Republic of Serbia'),
    ('SC', 'Republic of Seychelles'),
    ('SL', 'Republic of Sierra Leone'),
    ('SG', 'Republic of Singapore'),
    ('SX', 'Sint Maarten     (Dutch part)'),
    ('SK', 'Slovak Republic'),
    ('SI', 'Republic of Slovenia'),
    ('SO', 'Federal Republic of Somalia'),
    ('ZA', 'Republic of South Africa'),
    ('ES', 'Kingdom of Spain'),
    ('LK', 'Democratic Socialist Republic of Sri Lanka'),
    ('SD', 'Republic of the Sudan'),
    ('SR', 'Republic of Suriname'),
    ('SS', 'Republic of South Sudan'),
    ('SZ', 'Kingdom of Swaziland'),
    ('SE', 'Kingdom of Sweden'),
    ('CH', 'Swiss Confederation'),
    ('TW', 'Taiwan, Province of China'),
    ('TJ', 'Republic of Tajikistan'),
    ('TZ', 'United Republic of Tanzania'),
    ('TH', 'Kingdom of Thailand'),
    ('TL', 'Democratic Republic of Timor-Leste'),
    ('TG', 'Togolese Republic'),
    ('TO', 'Kingdom of Tonga'),
    ('TT', 'Republic of Trinidad and Tobago'),
    ('TN', 'Republic of Tunisia'),
    ('TR', 'Republic of Turkey'),
    ('UG', 'Republic of Uganda'),
    ('GB', 'United Kingdom of Great Britain and Northern Ireland'),
    ('US', 'United States of America'),
    ('UY', 'Eastern Republic of Uruguay'),
    ('UZ', 'Republic of Uzbekistan'),
    ('VU', 'Republic of Vanuatu'),
    ('VE', 'Bolivarian Republic of Venezuela'),
    ('VN', 'Socialist Republic of Viet Nam'),
    ('VG', 'British Virgin Islands'),
    ('VI', 'Virgin Islands of the United States'),
    ('YE', 'Republic of Yemen'),
    ('ZM', 'Republic of Zambia'),
    ('ZW', 'Republic of Zimbabwe'),
)

class CountryField(forms.ChoiceField):
    """
    Renders a select element populated with world countries.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the instance.
        """
        kwargs.setdefault('choices', COUNTRIES)
        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        """
        Returns internal class type.

        :rtype: str.
        """
        return 'ChoiceField'

class MailChimpForm(forms.Form):
    """
    MailChimp list-based form class.
    """
    def __init__(self, merge_vars, *args, **kwargs):
        """
        Initailizes the form instance, adding fields for specified
        MailChimp merge variables.

        :param merge_vars: list of merge variable dictionaries.
        """
        # Initialize the form instance.
        super(MailChimpForm, self).__init__(*args, **kwargs)

        # Add merge variable fields.
        for merge_var in merge_vars:
            for data in self.mailchimp_field_factory(merge_var).items():
                name, field = data
                self.fields.update({name: field})

    def mailchimp_field_factory(self, merge_var):
        """
        Returns a form field instance for specified MailChimp merge variable.

        :param merge_var: merge variable dictionary.
        :rtype: django.forms.Field.
        """
        fields  = OrderedDict()
        mc_type = merge_var.get('field_type', None)
        name    = merge_var.get('tag', '').lower()
        kwargs  = {
            'label':        merge_var.get('name', None),
            'required':     merge_var.get('req', True),
            'initial':      merge_var.get('default', None),
            'help_text':    merge_var.get('helptext', None)
        }
    
        if mc_type == 'email':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.EmailField(**kwargs)})
    
        if mc_type == 'text':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.CharField(**kwargs)})
    
        if mc_type == 'number':
            fields.update({name: forms.IntegerField(**kwargs)})
    
        if mc_type == 'radio':
            kwargs.update({
                'choices':  ((x, x) for x in merge_var.get('choices', [])),
                'widget':   forms.RadioSelect
            })
            fields.update({name: forms.ChoiceField(**kwargs)})
    
        if mc_type == 'dropdown':
            kwargs.update({
                'choices':  ((x, x) for x in merge_var.get('choices', []))
            })
            fields.update({name: forms.ChoiceField(**kwargs)})
    
        if mc_type == 'date' or mc_type == 'birthday':
            fields.update({name: forms.DateField(**kwargs)})
    
        if mc_type == 'address':
            # Define keyword agruments for each charfield component.
            char_fields = [
                {
                    'name':         '{0}-addr1'.format(name),
                    'label':        'Address',
                    'required':     True,
                    'max_length':   70,
                },
                {
                    'name':         '{0}-addr2'.format(name),
                    'label':        'Address Line 2',
                    'required':     True,
                    'max_length':   70,
                },
                {
                    'name':         '{0}-city'.format(name),
                    'label':        'Address',
                    'required':     True,
                    'max_length':   40,
                },
                {
                    'name':         '{0}-state'.format(name),
                    'label':        'State/Province/Region',
                    'required':     True,
                    'max_length':   20,
                },
                {
                    'name':         '{0}-zip'.format(name),
                    'label':        'Zip Code',
                    'required':     True,
                    'max_length':   10,
                },
            ]
    
            # Add the address charfields.
            for kwargs in char_fields:
                field_name = kwargs.pop('name')
                fields.update({field_name: forms.CharField(**kwargs)})
    
            # Finally, add the address country field.
            name = '{0}-country'.format(name)
            fields.update({name: CountryField(initial='US')})
    
        if mc_type == 'zip':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.CharField(**kwargs)})
    
        if mc_type == 'phone':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.CharField(**kwargs)})
    
        if mc_type == 'url' or mc_type == 'imageurl':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.URLField(**kwargs)})
    
        return fields
