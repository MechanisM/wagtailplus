#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains form class definitions.
"""
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
